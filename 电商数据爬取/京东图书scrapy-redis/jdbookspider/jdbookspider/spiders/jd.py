import json, re, scrapy
# 1. 导入类
from scrapy_redis.spiders import RedisSpider

# 2.继承类
class JdSpider(RedisSpider):
    name = 'jd'
    # 3.注释掉爬虫的域和起始的地址
    # allowed_domains = ['jd.com']
    # start_urls = ['https://pjapi.jd.com/book/sort?source=bookSort&callback=jsonp_1618663655364_73233']
    # 6.创建redis_key
    redis_key = 'aef'

    # 4.添加__init__方法
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        print(self.allowed_domains)
        # 5.传入爬虫类名
        super(JdSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        解析图书分类
        :param response:
        :return:
        """
        big_url_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dd/em/a/@href').extract()
        for url in big_url_list:
            for page in range(1, 101):
                book_url = 'https:' + url + f'&page={page}'
                yield scrapy.Request(
                    url=book_url,
                    callback=self.parse_s_url_page_response,
                    dont_filter=True
                )

    def parse_s_url_page_response(self, response):
        """
        解析小分类列表页
        :param response:
        :return:
        """
        url_list = response.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/a/@href').extract()
        for url in url_list:
            if 'http' in url:
                continue
            else:
                yield scrapy.Request(
                    url='https:' + url,
                    callback=self.parse_url_info_response,
                    dont_filter=True
                )

    def parse_url_info_response(self, response):
        """
        解析商品详情页,抓取标题信息
        :param response:
        :return:
        """
        item = {}
        title = response.xpath('//title/text()').extract()
        item['title'] = title
        print(item)
