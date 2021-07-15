# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from random import choice
from jdspider.settings import USER_AGENT_LIST
from selenium import webdriver
from scrapy.http import HtmlResponse
import time

'''创建替换UA中间件'''


class RandomAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = choice(USER_AGENT_LIST)
        request.headers['user-agent'] = ua

    def process_response(self, request, response, spider):
        '''判断状态码,优化爬虫'''
        status_code = response.status
        if status_code != 200:
            ua = choice(USER_AGENT_LIST)
            request.headers['user-agent'] = ua
            return request
        return response


'''创建selenium中间件'''


class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        url = request.url
        '''判断是否为起始url'''
        if 'https://phat.jd.com/10-183.html' in url:
            # 创建webdriver对象
            driver = webdriver.Chrome()
            driver.get(url)
            # 设置缺省等待时间，防止页面加载过慢导致报错
            driver.implicitly_wait(5)
            time.sleep(3)
            # 获取源码
            html_str = driver.page_source
            # 关闭页面退出driver
            driver.close()
            driver.quit()
            '''构造新的响应'''
            response = HtmlResponse(
                url=url,
                request=request,
                body=html_str,
                encoding='utf-8'
            )
            return response
