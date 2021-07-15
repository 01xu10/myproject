# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : Fangtianxia_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/16 18:28
# ------------------------------

import requests,re
from lxml import etree
from pprint import pprint
from openpyxl import Workbook

class Fang_spider(object):
    # 1.url+headers
    def __init__(self):
        self.start_url = 'https://gz.zu.fang.com/house-a074/i3{}/?rfss=1-46a78d070e4a9b08f6-62'
        self.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        self.wb=Workbook()
        self.sheet = self.wb.active
        self.sheet.append(['标题','位置','户型','面积','价格','距离地铁位置','朝向','出租方式'])

    # 2.发起请求
    def respone(self):
        for i in range(1, 80):
            start_urls =self.start_url.format(i)
            respone = requests.get(start_urls, headers=self.headers).text
            # pprint(respone)
            self.analysis_data(respone)

    # 3.解析数据
    def analysis_data(self,respone):
        html_str = etree.HTML(respone)
        # 房子标题
        house_title = html_str.xpath(r'//*[@id="rentid_D09_01_02"]/a/text()')[0].replace('�h','')
        # pprint(house_name)

        # 房子设施
        house = html_str.xpath('//*[@id="listBox"]/div[2]/dl[1]/dd/p[2]/text()')
        rent_way = house[0].replace('\r\n','').replace(' ','')
        house_type = house[1]
        house_area = house[2].replace('�O','')+'㎡'
        house_facing = house[3].replace('\r\n','').replace(' ','')
        # pprint(house_facing)

        # 距离地铁位置
        subway1 = html_str.xpath('//*[@id="rentid_D09_13_06"]/a[1]/span/text()')[0]
        subway = subway1.join([subway for subway in html_str.xpath('//*[@id="rentid_D09_01_07"]/p/span/text()')]).replace('。', '')
        # pprint(subway)

        # 房子地址
        house_add1 = html_str.xpath('//*[@id="rentid_D09_01_06"]/text()')
        house_add2 = html_str.xpath('//*[@id="rentid_D09_01_06"]/a/span/text()')
        address=''
        for h1,h2 in zip(house_add1,house_add2):
            address += h1+h2
        address.replace('�h','')

        # pprint(address)

        # 月租价格
        rental_price = html_str.xpath(r'//*[@id="listBox"]/div[2]/dl[1]/dd/div[2]/p/span/text()')[0]+'元/月'
        # pprint(rental_price)
        self.save_data(house_title,address,house_type,house_area,rental_price,subway,house_facing,rent_way)

    def save_data(self,house_title,address,house_type,house_area,rental_price,subway,house_facing,rent_way):
        self.sheet.append([house_title,address,house_type,house_area,rental_price,subway,house_facing,rent_way])

    # 3.执行函数
    def main(self):
        self.respone()
        self.wb.save('Guangzhou_rental_info.xlsx')

if __name__ == '__main__':
    print('*********正在写入租房信息*********')
    lagou = Fang_spider()
    lagou.main()


