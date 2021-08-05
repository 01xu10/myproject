# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : 自动化test
# @File    : login.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/8/4 14:45
# ------------------------------

"""
    接口名称：登录接口
    类型：token机制
    用途：
        1- 本身需要做接口自动化测试
        2- 获取token，给后续的接口做鉴权
"""
from configs.config import HOST
from jsonpath import jsonpath
from pprint import pprint
import requests
import hashlib


class Login(object):
    def login(self, in_data, mode=True):
        '''
        登陆方法
        :return:返回响应体字典
        '''
        # url路径
        url = f'{HOST}/api/loginS'
        in_data['password'] = self.get_md5(in_data['password'])
        # 参数
        payload = in_data
        # 请求
        response = requests.post(url, json=payload)
        # 获取token
        if mode:
            return ''.join(jsonpath(response.json(), '$..token'))
        # 获取响应数据
        else:
            return response.json()

    def get_md5(self, psw):
        '''
        md5加密
        :param psw:
        :return: 返回MD5加密值
        '''
        # 实例化md5对象
        md5 = hashlib.md5()
        # 调用加密方法进行加密
        md5.update(psw.encode('utf-8'))
        return md5.hexdigest()


if __name__ == '__main__':
    lg = Login()
    resp = lg.login({'username': '20154084', 'password': '123456'})
    pprint(resp)
