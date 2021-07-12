# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : 验证码识别.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/7/9 15:21
# ------------------------------

'''
    AppCode：	DEFBD93083C84FC0A9F5BA3CAAE0FFDE
    AppKey：	AKID6376ab070ac454c5bcbed9ede71bd2df
    AppSecret：	8047d9c787ed741c6f944d8fe8fa881c
'''
'''
import urllib, urllib.request, sys

host = 'http://apigateway.jianjiaoshuju.com'
path = '/api/v_1/yzmCrd.html'
method = 'POST'
appcode = '你自己的AppCode'
appKey = '你自己的AppKey'
appSecret = '你自己的AppSecret'
querys = ''
bodys = {}
url = host + path

bodys['v_pic'] = 'v_pic'
bodys['v_type'] = 'v_type'
post_data = urllib.urlencode(bodys)
request = urllib.Request(url, post_data)
request.add_header('appcode', appcode)
request.add_header('appKey', appKey)
request.add_header('appSecret', appSecret)
//根据API的要求，定义相对应的Content-Type
request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
response = urllib.urlopen(request)
content = response.read()
if (content):
    print(content)
'''
# 改造代码
# v_type	STRING
from requests_html import HTMLSession
from fake_useragent import UserAgent
session = HTMLSession()
ua = UserAgent()

headers = {
    'AppCode': 'DEFBD93083C84FC0A9F5BA3CAAE0FFDE',
    'AppKey': 'AKID6376ab070ac454c5bcbed9ede71bd2df',
    'AppSecret': '8047d9c787ed741c6f944d8fe8fa881c',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

data = {
    'v_pic': '',
    'v_type': ''
}

start_url = 'http://apigateway.jianjiaoshuju.com/api/v_1/yzmCrd.html'
