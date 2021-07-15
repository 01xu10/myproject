# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : xiecheng_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/11 12:23
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from pprint import pprint
from urllib.parse import quote
session = HTMLSession()
ua = UserAgent()

class epid_travel_spider(object):
    def __init__(self):
        self.start_url = 'https://you.ctrip.com/searchsite/travels/?query=%E7%96%AB%E6%83%85&PageNo=3'
        self.headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'

        }

    def parse_start_url(self):
        response = session.get(self.start_url,headers=self.headers)
        title_url_list = response.html.xpath('//ul[@class="youji-ul cf"]/li/a/@href')
        # pprint(title_url_list)
        for title_url in title_url_list:
            title_url = 'https://you.ctrip.com/' + title_url
            print(title_url)


if __name__ == '__main__':
    travel = epid_travel_spider()
    travel.parse_start_url()