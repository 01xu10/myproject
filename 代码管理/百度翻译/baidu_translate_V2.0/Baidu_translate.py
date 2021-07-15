# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : Baidu_translate.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/8 18:53
# ------------------------------

import requests
from pprint import pprint

class Baidu_Translation(object):

    # 1.url+headers
    def __init__(self,word):
        self.start_url = r'https://fanyi.baidu.com/sug'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36'
        }
        self.from_data = {
            'kw': word
        }
        
    # 2.发起请求
    def respone(self):
        respone = requests.post(self.start_url, headers=self.headers, data=self.from_data).json()
        # pprint(respone)
        self.analyze_data(respone)

    # 3.解析数据,获取翻译内容
    def analyze_data(self, respone):
        str = respone['data'][0]['v']
        print(str)

    # 4.执行程序
    def main(self):
        self.respone()


if __name__ == '__main__':
    word = input('请输入要翻译的内容：')
    translate = Baidu_Translation(word)
    translate.main()