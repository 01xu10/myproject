# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : anjuke_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/17 15:22
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from xlutils.copy import copy
import os, xlwt, xlrd
import re, time
session = HTMLSession()
ua = UserAgent()


class anjuke_spider(object):
    def __init__(self):
        self.start_url = 'https://gz.zu.anjuke.com/ditie/zj102-p{}/'
        self.headers = {
            'referer': 'https://gz.zu.anjuke.com/ditie/zj102-dt31/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'upgrade-insecure-requests': '1',
            'user-agent': ua.chrome
        }
        self.num = 1

    def parse_start_url(self):
        i = 1
        print('**************正在进入租房链接**************')
        time.sleep(2)
        while True:
            response = session.get(self.start_url.format(i), headers=self.headers)
            # print(response.text.replace('\n', '').replace('  ',''))
            if response.status_code != 200:
                break
            else:
                house_name_list = response.html.xpath('//*[@id="list-content"]/div/div[1]/h3/a/b/text()')
                house_url_list = response.html.xpath('//*[@id="list-content"]/div/div[1]/h3/a/@href')
                subway_list = re.findall('">距(.*?m)</span>', response.text)
                house_area_list = response.html.xpath('//*[@id="list-content"]/div/div/address/a/text()')
                house_address_list = re.findall('&nbsp;&nbsp;(.*?)</address>',
                                                response.text.replace('\n', '').replace('  ', ''))
                for house_name, house_url, subway, house_area, house_address in zip(house_name_list, house_url_list,
                                                                                    subway_list, house_area_list,
                                                                                    house_address_list):
                    subway = '距' + subway + 'm'
                    self.parse_house_url(house_name, house_url, subway, house_area, house_address)
                    break
            i += 1

    def parse_house_url(self, house_name, house_url, subway, house_area, house_address):
        '''

        :param house_name:      房子名称
        :param house_url:       房子链接
        :param subway:          房子地铁
        :param house_area:      房子小区
        :param house_address:   房子地址
        :return:
        '''
        print('---------------正在进入获取房源信息---------------')
        time.sleep(1)
        list_1 = ['室', '厅', '卫']
        house_hx = ''
        response = session.get(house_url, headers=self.headers)
        '''租房价格'''
        house_price = response.html.xpath('//span[@class="price"]/em/b/text()')[0] + '元/月'
        '''支付规则'''
        payment_rule = response.html.xpath('//li[@class="full-line cf"]/span[2]/text()')[0]

        house_detail = response.html.xpath('//div[@class="auto-general"][1]/b/text()')
        '''房源概况'''
        house_detail = ' '.join(house_detail).replace('\n', '')
        '''出租要求'''
        rent_rule = ''.join(response.html.xpath('//div[@class="auto-general"][2]/b/text()'))
        '''设施'''
        house_equipment = ','.join(response.html.xpath('//li[@class="peitao-item has"]/div/text()'))
        '''发布时间'''
        house_issue_time = response.html.xpath('//span[@id="houseCode"]/../b/text()')[0]
        '''户型'''
        house_hx_1 = response.html.xpath('//span[@class="info"]/b/text()')[:-1]
        for i, j in zip(house_hx_1, list_1):
            house_hx += i + j
        '''房子大小'''
        house_size = response.html.xpath('//span[@class="info"]/b/text()')[-1]
        '''房子朝向，楼高，装修，类型'''
        house_item_list = response.html.xpath('//li[@class="house-info-item"]/span[2]/text()')[3:]
        house_cx = house_item_list[0]
        house_height = house_item_list[1]
        house_decoration = house_item_list[2]
        house_type = house_item_list[3]
        print(house_issue_time, house_name, house_hx, house_size, house_price, rent_rule, payment_rule, house_address, house_area, subway, house_equipment, house_cx, house_height, house_decoration, house_type, house_detail)
        house_list = [house_issue_time, house_name, house_hx, house_size, house_price, rent_rule, payment_rule, house_address, house_area, subway, house_equipment, house_cx, house_height, house_decoration, house_type, house_detail]
        house_dict = {
            '租房信息': house_list
        }
        self.save_excel(house_dict)
        print('=================第{}条数据爬取成功！！！=================='.format(self.num))
        self.num += 1

    def save_excel(self, data):
        # data = {
        #     '基本详情': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        # }
        os_path_1 = os.getcwd() + '/租房数据/'
        if not os.path.exists(os_path_1):
            os.mkdir(os_path_1)
        # os_path = os_path_1 + self.os_path_name + '.xls'
        os_path = os_path_1 + '租房信息.xls'
        if not os.path.exists(os_path):
            # 创建新的workbook（其实就是创建新的excel）
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建新的sheet表
            worksheet1 = workbook.add_sheet("租房信息", cell_overwrite_ok=True)
            borders = xlwt.Borders()  # Create Borders
            """定义边框实线"""
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 0x40
            borders.right_colour = 0x40
            borders.top_colour = 0x40
            borders.bottom_colour = 0x40
            style = xlwt.XFStyle()  # Create Style
            style.borders = borders  # Add Borders to Style
            """居中写入设置"""
            al = xlwt.Alignment()
            al.horz = 0x02  # 水平居中
            al.vert = 0x01  # 垂直居中
            style.alignment = al
            # 合并 第0行到第0列 的 第0列到第13列
            '''基本详情13'''
            # worksheet1.write_merge(0, 0, 0, 13, '基本详情', style)
            excel_data_1 = ('发布时间', '房子名称', '户型', '大小', '租房价格', '出租要求', '支付规则', '位置', '小区', '地铁', '设施', '朝向', '楼高', '装修', '类型', '房源概况')
            for i in range(0, len(excel_data_1)):
                worksheet1.col(i).width = 2560 * 3
                #               行，列，  内容，            样式
                worksheet1.write(0, i, excel_data_1[i], style)
            workbook.save(os_path)
        # 判断工作表是否存在
        if os.path.exists(os_path):
            # 打开工作薄
            workbook = xlrd.open_workbook(os_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_path)

if __name__ == '__main__':
    a = anjuke_spider()
    a.parse_start_url()
