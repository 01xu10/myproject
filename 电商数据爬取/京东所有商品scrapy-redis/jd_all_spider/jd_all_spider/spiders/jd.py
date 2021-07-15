# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
import json, re, jsonpath


class JdSpider(RedisSpider):
    name = 'jd'
    # allowed_domains = ['jd.com']
    # start_urls = ['https://www.jd.com/']
    redis_key = 'ace'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        # 5.传入爬虫类名
        super(JdSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        解析商品大分类
        :param response:
        :return:
        """
        # big_url_list = response.xpath('//*[@id="J_cate"]/ul/li/a/@href').extract()
        # # print(big_url_list)
        # big_name_list = response.xpath('//*[@id="J_cate"]/ul/li/a/text()').extract()
        # # print(big_name_list)
        yield scrapy.Request(
            url='https://dc.3.cn/category/get?&callback=getCategoryCallback',
            callback=self.parse_next_url_response,
            dont_filter=True
        )

    def parse_next_url_response(self, response):
        """
        解析响应为小分类的地址，过滤活动页面
        :param response:
        :return:
        """
        json_data_str_obj = response.body.decode('gbk')
        json_data_str = ''.join(re.findall(r'getCategoryCallback\((.*?)\)', json_data_str_obj))
        json_data = json.loads(json_data_str)['data']
        s_list = jsonpath.jsonpath(json_data, '$..n')
        result = [i.split('|')[0] for i in s_list]
        '''数据清洗'''
        for i in result:
            if (i is None) or (i == '') or ('www' in i) or ('caipiao' in i) or ('bao.jd.com' in i) or (
                    'dujia.jd.com' in i):
                continue
            elif ('sale.jd.com' in i) or ('pro' in i) or ('mall' in i) or ('chongzhi.jd.com/' in i) or ('xinfang' in i):
                continue
            elif ('z.jd.com' in i) or ('jipiao.jd.com' in i) or ('mvd.jd.com' in i):
                continue
            '''把含有list的url全部提取出来'''
            if 'list' in i:
                # print(i)
                for page in range(1, 101):
                    """构造详情页地址请球对象"""
                    yield scrapy.Request(
                        url='https://' + i + f'&page={page}',
                        callback=self.parse_list_page_response,
                        dont_filter=True
                    )
            '''通过id，拼接小分类url'''
            if ('-' in i) and ('/' not in i):
                for page in range(1, 101):
                    next_url = 'https://list.jd.com/list.html?cat=' + i.replace('-', ',') + f'&page={page}'
                    # print(next_url)
                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse_list_page_response,
                        dont_filter=True
                    )

    def parse_list_page_response(self, response):
        """
        解析商品列表页响应，提取每个商品的id，拼接详情页url
        :param response:
        :return:
        """
        # allow_redirects=False
        data_spu_list = response.xpath('//*[@id="J_goodsList"]/ul/li/@data-spu').extract()
        for data_spu in data_spu_list:
            spu_url = f'https://item.jd.com/{data_spu}.html'
            yield scrapy.Request(
                url=spu_url,
                callback=self.parse_shop_info_response,
                meta={'shop_id': data_spu, 'proxy': 'http://139.224.74.219:16817'},
                dont_filter=True,
            )

    def parse_shop_info_response(self, response):
        """
        解析商品详情页响应
        :param response:
        :return:
        """
        print(response.url)
        # 商品id
        shop_id = response.meta['shop_id']
        # 商品名称
        title = response.xpath('//title/text()').extract()
        # 商品品牌名称
        shop_title = response.xpath('//ul[@class="p-parameter-list"]/li/a/text()').extract()
        # 商品数据
        shop_data = response.xpath('//*[@id="parameter2"]/li/text()').extract()
        # 商品价格接口
        price_url = f'https://p.3.cn/prices/mgets?skuIds={shop_id}'
        yield scrapy.Request(
            url=price_url,
            callback=self.parse_shop_price_data,
            meta={'title': title, 'shop_title': shop_title, 'shop_data': shop_data},
            dont_filter=True
        )

    def parse_shop_price_data(self, response):
        """
        解析商品价格
        :param response:
        :return:
        """
        item = {}
        title = response.meta['title']
        item['title'] = title
        shop_title = response.meta['shop_title']
        item['shop_title'] = shop_title
        shop_data = response.meta['shop_data']
        item['shop_data'] = shop_data
        response_str = response.body.decode()
        price = ''.join(re.findall(r'"p":"(.*?)"', response_str))
        item['price'] = price
        print(item)
        print()
        print()
        yield item
