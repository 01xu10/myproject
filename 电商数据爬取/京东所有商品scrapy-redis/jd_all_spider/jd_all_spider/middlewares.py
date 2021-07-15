# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from jd_all_spider.settings import USER_AGENT_LIST
from w3lib.http import basic_auth_header
import random, base64


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        start_url = request.url
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua


class ProxyMiddleware(object):
    '''ip代理 '''
    def process_request(self, request, spider):
        proxy = '139.224.74.219:16817'
        request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
        # meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
        # meta['proxy'] = 'http://139.224.74.219:16817'
        # 用户名密码认证(私密代理/独享代理)
        request.headers['Proxy-Authorization'] = basic_auth_header('${s403411124}', '${80i9bdkq}')  # 白名单认证可注释此行
        return None










