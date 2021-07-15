# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from jdbookspider.settings import USER_AGENT_LIST, IP_PROXY_LIST
import random, base64, time
from scrapy.http import HtmlResponse


class UserAgentMiddleware(object):
    '''替换ua'''
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua


class ProxyMiddleware(object):
    '''ip代理'''
    def process_request(self, request, spider):
        proxy = IP_PROXY_LIST[0]
        base64_data = base64.b64encode(proxy['user_passwd'].encode()).decode()
        request.headers['Proxy-Authorization'] = 'Basic ' + base64_data
        request.meta['proxy'] = proxy['ip_port']


class ParseStartUrlMiddleware(object):
    '''用selenium抓取网页html结构'''
    def process_request(self, request, spider):
        start_url = request.url
        if 'book.jd.com/booksort' in start_url:
            driver = webdriver.Chrome()
            driver.get(start_url)
            time.sleep(5)
            html_str = driver.page_source
            driver.close()
            response = HtmlResponse(
                url=start_url,
                request=request,
                body=html_str,
                encoding='UTF-8'
            )
            return response




