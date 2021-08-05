# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : 自动化test
# @File    : conftest.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/8/4 18:03
# ------------------------------

import pytest


# 自动化测试执行前---设置初始化环境操作
@pytest.fixture(scope='session', autouse=True)
def start_running():
    print('------马上开始执行自动化测试------------------')
    yield
    print('------自动化测试完成，开始处理垃圾数据---------')
# 自动化测试完后清除操作
