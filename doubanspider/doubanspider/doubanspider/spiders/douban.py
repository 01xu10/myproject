# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    ua = UserAgent()
    # start_urls = ['http://douban.com/']
    # https://movie.douban.com/top250?start=25&filter=
    headers = {
        'user-agent': ua.chrome
    }

    """
    类继承，调用父类方法，重写父类方法
    """
    # 重写scrapy爬虫框架，起始的请求
    def start_requests(self):
        i = 0
        for page in range(10):
            start_url = f'https://movie.douban.com/top250?start={25*page}&filter='

            yield scrapy.Request(
                url=start_url,
                headers=self.headers,
                callback=self.parse,
                meta={'i': i}
            )
            i += 1

    def parse(self, response):
        """
        解析响应
        :param response:
        :return:
        """
        # 获取循环计数
        i_num = response.meta['i']
        # 提取电影的标题
        title_list = response.xpath(
            '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()'
        ).extract()
        """
        .extract():从xpath对象中提取内容数据
        """
        # 提取电影的详情页链接
        href_list = response.xpath(
            '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href'
        ).extract()
        for href, title in zip(href_list, title_list):
            yield scrapy.Request(
                url=href,
                headers=self.headers,
                # callback 回调指定   指定这个地址的响应，由谁来解析
                callback=self.parse_href_response,
                # meta的作用：数据的传递
                meta={'db': title, 'num': i_num}
            )
            i_num += 1

    def parse_href_response(self, response):
        """
        解析电影的详情页的响应
        :param response: 电影的详情页的响应
        :return:
        """
        # 循环计数
        page = response.meta['num']
        item = {}
        # 获取meta中的value
        title = response.meta['db']
        item['title'] = title
        # 提取电影的剧情简介
        span_text = response.xpath(
            '//*[@id="link-report"]/span[1]/text()'
        ).extract()
        item['span_text'] = span_text
        yield item





