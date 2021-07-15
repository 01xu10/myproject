# -*- coding: utf-8 -*-
import scrapy, json
'''
   箱包分类xpath //ul[@class="quark-5cb43f1780772100479b2052__nav-channel__tabs"]/li/nav/a/@href
   价格接口 https://p.3.cn/prices/mgets?skuids={sku_id}
'''

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://phat.jd.com/10-183.html']

    def parse(self, response):
        '''
            解析箱包页面，获取各分类url
            通过解析网页，发现页面渲染结构和网页源码结构不一样，使用xpath提取不到
            经过分析，各分类的链接可以通过（协议+标签名）拼接url，则使用selenium获取页面信息，再通过xpath提取
        :param response:
        :return:
        '''
        '''提前分类链接'''
        type_url_list = response.xpath('//ul[@class="quark-5cb43f1780772100479b2052__nav-channel__tabs"]/li/nav/a/@href').extract()
        type_name_list = response.xpath('//ul[@class="quark-5cb43f1780772100479b2052__nav-channel__tabs"]/li/nav/a/span/text()').extract()
        for type_url, type_name in zip(type_url_list, type_name_list):
            print(type_url, type_name)
            if 'https:' not in type_url:
                type_url = 'https:' + type_url
                print(type_url, type_name)
            yield scrapy.Request(
                url=type_url,
                callback=self.parse_type_url
            )
            break

    def parse_type_url(self, response):
        '''
        解析各分类url，通过xpath获取
        :param response:
        :return:
        '''
        brand_url_list = response.xpath('//ul[@class="J_valueList v-fixed"]/li/a/@href').extract()
        # print(len(brand_url_list), brand_url_list)
        for brand_url in brand_url_list:
            brand_url = 'https://search.jd.com/' + brand_url
            print(brand_url)
            yield scrapy.Request(
                url=brand_url,
                callback=self.parse_brand_page
            )
            break

    def parse_brand_page(self, response):
        '''
        解析品牌页面，获取商品url，通过xpath获取
        :param response:
        :return:
        '''
        commodity_url_list = response.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/@href').extract()
        # print(goods_url)
        commodity_name_list = response.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a')
        for commodity_url, commodity_name in zip(commodity_url_list, commodity_name_list):
            commodity_url = 'https:' + commodity_url
            # print(commodity_url)
            yield scrapy.Request(
                url=commodity_url,
                callback=self.parse_item_info,
                meta={'name': commodity_name}
            )
            break

    def parse_item_info(self, response):
        '''
        解析商品详情页，通过xpath获取，价格没有存在网页源码中
        通过抓包，找到价格接口，通过id匹配各商品价格
        :param response:
        :return:
        '''
        '''商品名称'''
        item_name = response['name']
        # print(item_name)
        '''商品详情信息'''
        item_detail = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li/text()').extract()
        # print(item_detail)
        '''商品id'''
        sku_id = response.url[20:-5]
        # print(sku_id)
        '''商品价格接口'''
        yield scrapy.Request(
            url=f'https://p.3.cn/prices/mgets?skuids={sku_id}',
            callback=self.save_item,
            meta={'detail': item_detail, 'name': item_name},
            dont_filter=True
        )

    def save_item(self, response):
        '''
        保存数据，解析价格页面，转换为json数据
        :param response:
        :return:
        '''
        '''商品信息'''
        item_detail_data = response['detail']
        '''商品名称'''
        item_name = response['name']
        '''商品价格'''
        data = response.body.decode()
        list_data = json.loads(data)
        price = list_data[0]['p']
        '''把价格和名称插入详情信息'''
        item_detail_data.insert(1, price)
        item_detail_data.insert(0, item_name)
        item = {'data': item_detail_data}
        print('************************************************')
        yield item

