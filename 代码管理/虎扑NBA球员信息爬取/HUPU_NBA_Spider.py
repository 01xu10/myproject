# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : HUPU_NBA_Spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/12 19:31
# ------------------------------

import requests
from lxml import etree
from pprint import pprint
from openpyxl import Workbook


class NBA_numbers(object):
    # 1.url+headers+excel
    def __init__(self):
        self.start_url = r'https://nba.hupu.com/players'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        self.wb = Workbook()
        self.sheet = self.wb.active
        self.sheet.append(['姓名','英文名','号码','位置','身高','体重','生日','合同'])



    # 2.发起请求
    def request(self):
        respone = requests.get(self.start_url, headers=self.headers).text
        html_str = etree.HTML(respone)
        nba_urls = html_str.xpath(r'//ul/li/span/a/@href')
        nba_teams = html_str.xpath(r'//ul/li/span/a/text()')
        # 3.对每个球队发起请求
        for nba_url,nba_team in zip(nba_urls,nba_teams):
            self.analysis_data(nba_url)

    # 3.分析数据，爬取NBA球员的个人信息
    def analysis_data(self,nba_url):
        respone = requests.get(nba_url,headers=self.headers).text
        html_str = etree.HTML(respone)
        nba_names= html_str.xpath(r'//td[2]/b/a/text()')
        nba_Eng_names = html_str.xpath(r'//td[2]/p/b/text()')
        nba_nums = html_str.xpath(r'//td[3]/text()')[1::]
        nba_adds = html_str.xpath(r'//td[4]/text()')[1::]
        nba_heights = html_str.xpath(r'//td[5]/text()')[1::]
        nba_weights = html_str.xpath(r'//td[6]/text()')[1::]
        nba_birs = html_str.xpath(r'//td[7]/text()')[1::]
        nba_coms = html_str.xpath(r'//td[8]/text()')[1::]
        nba_ms = html_str.xpath(r'//td[8]/b/text()')
        for nba_name,nba_Eng_name,nba_num,nba_add,nba_height,nba_weight,nba_bir,nba_com,nba_m in zip(nba_names,nba_Eng_names,nba_nums,nba_adds,nba_heights, nba_weights, nba_birs, nba_coms, nba_ms):
            #1111
            self.save_imfo(nba_name, nba_Eng_name,nba_num,nba_add,nba_height,nba_weight,nba_bir,nba_com,nba_m)

    # 4.保存数据
    def save_imfo(self,nba_name, nba_Eng_name,nba_num,nba_add,nba_height,nba_weight,nba_bir,nba_com,nba_m):
        self.sheet.append([nba_name, nba_Eng_name,nba_num,nba_add,nba_height,nba_weight,nba_bir,nba_com+nba_m])

    # 5.执行函数
    def main(self):
        self.request()
        self.wb.save('NBA_player_info.xlsx')

if __name__ == '__main__':
    numbers = NBA_numbers()
    numbers.main()
