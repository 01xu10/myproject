# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : qimingpian_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/7/8 16:28
# ------------------------------

'''
    爬取创业项目
    1.观察数据，异步加载
    2.抓包，数据被加密
    3.搜索加密参数，添加断点，观察生成密文函数
    4.通过execjs，逆向解析
'''

from requests_html import HTMLSession
from fake_useragent import UserAgent
from pprint import pprint
import execjs, json
session = HTMLSession()
ua = UserAgent()

class qimingpian_spider(object):
    def __init__(self):
        self.start_url = 'https://vipapi.qimingpian.com/DataList/productListVip'
        self.headers = {
            'user-agent': ua.chrome,
            'Host': 'vipapi.qimingpian.com',
            'Origin': 'https://www.qimingpian.cn'
        }
        self.form_data = 'time_interval=&tag=&tag_type=and&province=&lunci=&page=3&num=20&unionid=5iXsAiiF%2BSM2QopTrSrfjoQQPlWDSh1tb1mjkRUNgGWgY2lN%2FBpu%2BqtxxufAukk%2FeJWqqIs6kiQsM8IbOYgM5A%3D%3D'

    def parse_start_url(self):
        '''
        解析网页，获取加密数据
        :return:
        '''
        response = session.post(self.start_url, headers=self.headers, data=self.form_data).json()
        # print(response)
        encrypt_data = response['encrypt_data']
        # print(encrypt_data)
        jscode = self.load_jscode('./qiming.js')
        '''执行js代码'''
        # compile(js代码) call('o'， 加密字段)
        rst = execjs.compile(jscode).call('o', encrypt_data)
        # print(rst)
        '''模拟javascrpit代码中的JSON.parse方法'''
        json_data = json.loads(rst)
        '''解析完成'''
        # pprint(json_data)
        self.parse_data(json_data)


    def load_jscode(self, path):
        '''
        加载js代码
        :param path:
        :return:
        '''
        with open(path, 'r', encoding='utf-8')as f:
            js_code = f.read()
        return js_code

    def parse_data(self, json_data):
        data_list = json_data['list']
        for data in data_list:
            '''公司名称'''
            product = data['product']
            '''公司行业'''
            business = data['hangye1']
            '''公司业务'''
            operation = data['yewu']
            '''省份'''
            province = data['province']
            '''公司阶段'''
            stage = data['jieduan']
            '''投资'''
            money = data['money']
            '''时间'''
            time = data['time']
            print('******************************************')
            print(product, business, operation, province, stage, money, time)



if __name__ == '__main__':
    qm = qimingpian_spider()
    qm.parse_start_url()