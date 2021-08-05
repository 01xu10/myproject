# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : 自动化test
# @File    : test_login.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/8/4 15:46
# ------------------------------
# from tools.yamlControl import get_yaml_data
# from libs.login import Login
# from pprint import pprint
#
# # 执行用例
#
# # 1-获取用例数据
# res = get_yaml_data('../data/loginCase.yaml')[1]
#
# # 2-调用接口方法
# resp_data = Login().login(res['data'], False)
#
# # 3-断言
# if resp_data['message'] == res['resp']['message']:
#     print('----------用例通过----------')

from libs.login import Login
from tools.yamlControl import get_yaml_data
import pytest
import allure
import os
'''
    需求：登录有5个测试用例
    方案：数据驱动---读取用例数据---给pytest框架执行
        1- 用例的请求数据
        2- 用例的期望结果
'''

# 登录接口-测试类封装
class TestLogin(object):
    # 测试方法
    @pytest.mark.parametrize('in_body, exp_data', get_yaml_data('../data/loginCase.yaml'))
    def test_login(self, in_body, exp_data):
        # 调用业务层代码
        resp = Login().login(in_body, False)
        # 断言
        assert resp['message'] == exp_data['message']


if __name__ == '__main__':
    pytest.main(['test_login.py', '-s', '--alluredir', '../report/tmp'])
    # -s 打印 输出 使用allure产生报告
    os.system('allure serve ../report/tmp')
    '''
        F 用例失败  E error  . 成功
    '''
    '''
    allure报告方案原理：
        1- 生成报告所需的文件
        2- 使用一些工具打开可视化报告
    
    '''
