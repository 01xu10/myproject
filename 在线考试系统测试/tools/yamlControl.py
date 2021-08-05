# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : 自动化test
# @File    : yamlControl.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/8/4 15:36
# ------------------------------
import yaml


def get_yaml_data(file_dir):
    """
    :param file_dir:
    :return:
    """
    # [(请求1，期望响应1),(请求2，期望响应2)]
    res_list = []
    # 1 - 读取文件操作 - --从磁盘读取文件
    with open(file_dir, 'r', encoding='utf-8')as f:
        # 2-使用yaml方法读取文件
        res = yaml.load(f, Loader=yaml.FullLoader)
        del res[0]
        # 3-根据需求返回对应类型
        for i in res:
            res_list.append((i['data'], i['resp']))
        return res_list


if __name__ == '__main__':
    res = get_yaml_data('../data/loginCase.yaml')
    for i in res:
        print(i)
