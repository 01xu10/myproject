# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : TB_commodity_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/15 17:18
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from urllib.parse import quote
session = HTMLSession()
ua = UserAgent()

class TB_spider(object):
    def __init__(self):
        self.start_url = 'https://s.taobao.com/search?q={}'
        self.headers = {
            'cookie': 'cna=esBjGPb+5ysCAXjmfgYrwjLT; t=39ed7c7b49084a7d96127f0a38cb7537; miid=1172226141183772509; sgcookie=E100aobgSKAycYmYZhP9Q%2Fr8x4cy2zYMtjeFePnNwjfqVt8u0DOa8NP2AosR2%2FyFy3%2BsxoDtbZ0x4lNWyaMuEfamjQ%3D%3D; uc3=lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=qG4xH1%2BrhA9Q1R3bBUhyrTOKMxbBow%3D%3D&vt3=F8dCuwucBtLIdu956Rc%3D&id2=UUGrf6z4e6WENQ%3D%3D; lgc=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; uc4=nk4=0%40qlXnga8AYEMW1VrMSD5nndqSKiKIw4X3y0VR0u6CGhMS&id4=0%40U2OcT2LaNdpEAsP2rjbpg%2BDn4QEj; tracknick=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; _cc_=V32FPkk%2Fhw%3D%3D; enc=kDq%2FKkNRBYPT6WFwzCS45lXiFr8IsWfuC3nAJ%2FEGk5YCBpkIiQD4LsXs4%2B2peY7l9%2BgG7uCxJFMx0CZrtneoCw%3D%3D; mt=ci=6_1; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=5c89c8e1121d52321d47eb57049e057e_1618485344993; _m_h5_tk_enc=62f5f540efe5d45f250b7deb0598c17e; _tb_token_=e5333e7633a31; xlly_s=1; cookie2=158cc8a4a1d12a6f007c1f095b9b8da1; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=4BC5191C85253530A5D0925C46DE39B4; uc1=cookie14=Uoe1iuSwzi7ILg%3D%3D; tfstk=cYAABR6Xh0mDPy_J8KHu5w2M7rRAapzAjrsT6qHYcnY-GAVzZsYwtBpCKx_aD_3R.; l=eBL4gVJVjMf9BxeBBO5BFurza779aIRb4FVzaNbMiInca6CfTEmF0NCQWyT97dtjgt1pFetPbQoCndLHR3AiVh9N33h2q_7qnxf..; isg=BKSkEP8CmG8_JOxsysuLPSMUdaKWPcinXQ1Wa77F4m8OaUQz5kyUN9rDLcHxhAD_',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'upgrade-insecure-requests': '1',
            'referer': 'https://login.taobao.com/',
            'user-agent': ua.chrome
        }

    def parse_search_url(self):
        print('*********欢迎来的小旭淘宝店***********')
        commodity_1 = input('请输入查询的商品名称：')
        commodity = quote(commodity_1)
        print(commodity)
        response = session.get(self.start_url.format(commodity),headers=self.headers)
        print(response.content.decode())

    def main(self):
        self.parse_search_url()


if __name__ == '__main__':
    tb = TB_spider()
    tb.main()