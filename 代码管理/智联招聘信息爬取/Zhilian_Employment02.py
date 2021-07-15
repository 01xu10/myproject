# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : Zhilian_Employment02.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/3/1 14:03
# ------------------------------

import requests, json, jsonpath
from xlutils.copy import copy
import os, xlwt, xlrd
from lxml import etree
from pprint import pprint
from openpyxl import Workbook


class Employment(object):
    def __init__(self):
        self.city_select = input('请输入:')
        self.position = input('请输入你要搜索的职位:')
        self.start_url = 'https://fe-api.zhaopin.com/c/i/search/positions?at=115f1d9013f742dc888f1a221a9dc128&rt=078cc3e78270498f809432a39525de0d'
        self.headers = {
            'content-type': 'application/json; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        }
        self.citys = {"北京": "530", "上海": "538", "广州": "763", "深圳": "756", "天津": "531", "武汉": "736", "西安": "854",
                      "成都": "801",
                      "大连": "600", "长春": "613", "沈阳": "599", "南京": "635", "福州": "681", "厦门": "682", "哈尔滨": "622"}
        self.city = self.citys[self.city_select]
        self.num = 0
        self.pageIndex = 1
        self.payload_1 = {"S_SOU_FULL_INDEX": "", "S_SOU_WORK_CITY": "", "pageSize": 30, "pageIndex": 1, "cvNumber": "JI890106067R90500000000", "eventScenario": "pcSearchedSouSearch"}
        self.payload_1["S_SOU_WORK_CITY"] = self.city
        self.payload_1["S_SOU_FULL_INDEX"] = self.position

    def parse_url(self):
        while True:
            self.payload_1["pageIndex"] = self.pageIndex
            self.play_load = json.dumps(self.payload_1)
            respone = requests.post(url=self.start_url, headers=self.headers, data=self.play_load).json()
            # pprint(respone)
            isEndPage = jsonpath.jsonpath(respone, '$..isEndPage')[0]
            # pprint(isEndPage)
            if isEndPage == 0:
                self.analysis_data(respone)
            else:
                self.analysis_data(respone)
                print('')
                print('下载完毕，共{}页'.format(self.pageIndex))
                break
            self.pageIndex += 1

    def analysis_data(self, respone):
        lists = jsonpath.jsonpath(respone, '$..list')[0]
        for list in lists:
            name = list['name']
            workCity = list['workCity']
            workType = list['workType']
            companyName = list['companyName']
            cityDistrict = list['cityDistrict']
            education = list['education']
            property = list['property']
            salary60 = list['salary60']
            salaryCount = list['salaryCount']
            welfareLabel = ','.join([welfare['value'] for welfare in list['welfareLabel']])
            workingExp = list['workingExp']
            area = workCity + '-' + cityDistrict
            salary = salary60 + '   ' + salaryCount
            self.num += 1
            print(name, area, salary, workingExp, education, workType, companyName, property,welfareLabel)
            post_list = [name, area, salary, workingExp, education, workType, companyName, property, welfareLabel]
            data = {
                '招聘信息': post_list
            }
            self.save_excel(data)
            # break
            print('\r***已下载完成了：{}条招聘信息***'.format(self.num), end='')

    def save_excel(self, data):
        # data = {
        #     '基本详情': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        # }
        os_path_1 = os.getcwd() + '/招聘信息/'
        os.makedirs(os_path_1, exist_ok=True)
        # os_path = os_path_1 + self.os_path_name + '.xls'
        os_path = os_path_1 + '{}_post_info.xls'.format(self.position)
        if not os.path.exists(os_path):
            # 创建新的workbook（其实就是创建新的excel）
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建新的sheet表
            worksheet1 = workbook.add_sheet("招聘信息", cell_overwrite_ok=True)
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
            excel_data_1 = ('职位', '位置', '薪水', '工作经验', '学历', '工作性质', '公司名称', '公司类型', '福利')
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
    print('---------招聘信息-----------')
    print('*****请选择你要工作的城市*****')
    print("北京, 上海, 广州, 深圳, 天津, 武汉, 西安, 成都, 大连, 长春, 沈阳, 南京, 福州 ,厦门 ,哈尔滨")
    employee = Employment()
    employee.parse_url()
'''
    https://fe-api.zhaopin.com/c/i/search/positions?at=115f1d9013f742dc888f1a221a9dc128&rt=078cc3e78270498f809432a39525de0d&_v=0.02517481&x-zp-page-request-id=14798928e0eb4788abe6afb75f7255bf-1619327569198-585891&x-zp-client-id=57f8f5c9-53c5-4e4c-a79f-a48fd79337bc&MmEwMD=5d1cASaf1M1vn.fLbYpD6HwaJpNknfTDNjTCwHqqCgVcdlalCRm9xbJt7nB7KAWAFbWtl_SOpFmYS0oNkduv2r9iI_N9pLmWdbnGyfRZq3MWCm3bIPDwpmXKEssEjKLA.gRhmg3g6c2pvci1zngAGplAM7els_vZ_Bnd1c41wakCHf9EMRcIfrluK2O3xjspKjlxVgVZoVqse9tHYFHzg3GbKyYrTjHqm8KBRjgyQOAOhbQU_C06OnktL.c33KlVsZG6zJBMmg0lPU23p.0cUbBXTUjWDeX3y2wVjm6S6lH9DaQLPTNs1B87IWizOg4MU_LOV4q1KhWSi6fuJd4CftOc6yDYwt.csefohVa8iOIMC53EmwMiK6adz8f_yeq8dRzQasaFcgvo4aVES2PqIoK65NbR1FNJV1chcMx2k7toW626v9rATBRUalbLzMBqz0nN
    https://fe-api.zhaopin.com/c/i/search/positions?at=115f1d9013f742dc888f1a221a9dc128&rt=078cc3e78270498f809432a39525de0d&_v=0.75859058&x-zp-page-request-id=14798928e0eb4788abe6afb75f7255bf-1619327569198-585891&x-zp-client-id=57f8f5c9-53c5-4e4c-a79f-a48fd79337bc&MmEwMD=56qDSyP2usqOsOu7owkcKoH07R4osNvcEPvnZo1lUaDD8WPqUpUGLXIiJ_eL638V4X8i2nOva1UpAZYzP6fOlxCt5a8YC61YI0A9jX.bMOp9drAClymua8NWqzZcj0_l7PUPT6MQQgqvyF26wsiIgBIN3YGUTKCOuyURQhlaGVSn3lp1JejMsMzrHPvT0Ay.a2WXignzwfN5RCUTAUUNaM4s51LBsFcQG8k7jHa4jcPKUyeIY7uHM0Hckl1P7oKMppUxwWKEF.F8ASEMs4JFxoyQOG1I0neMp3TAkUsJ5OGwRpIkjdR7ERGegnu8yaxvtRUhythfuFdlWw0gKFqCO1j0jbVsJA2vRtgjz4vF6Me8RpIDdZwGuJRoqgNUlGPvacMGnpGq_IvIGgAwvEfFAnJ6sbqEZ.2O4beDuvRwQpvM.jWWNo84J7j60sVQ080ph3Xf
    https://fe-api.zhaopin.com/c/i/search/positions?at=115f1d9013f742dc888f1a221a9dc128&rt=078cc3e78270498f809432a39525de0d&_v=0.22532911&x-zp-page-request-id=14798928e0eb4788abe6afb75f7255bf-1619327569198-585891&x-zp-client-id=57f8f5c9-53c5-4e4c-a79f-a48fd79337bc&MmEwMD=56qDSyP2usqOsOu7owkcKoH07R4osNvcEPvnZo1lUaDD8WPqUpUGLXIiJ_eL638V4X8i2nOva1UpAZYzP6fOlxCt5lim4I1ki.3AyOMEsMOv8LtMQPXfqein4jjSP7htn8I13.KFFiwuJ9DciP1gTpuwu6xxHb2y28TX8Kv5.lZhuHn1yfUmhVWl3AxHHUkeH00CrVHucC5_c4qj6pubExGZ.eYHqFbaZjIJr4BTMpI_BBTb8g1VCueMylMJOTaPp_Z4iOsJas5ODjtB3EPA9WvtPczbt3xGGTD5WiiooYL7bhNfzaCbYIUG6Wgys3VbZAD4fvfp1fCUSdHKAXN2sKFQyTlrmWu.lvkYufhmP8jQp.byzBL.B9dAJzebsUW.jf.GjrjUP.Nj1p9PfGSfqN4eJHo9qyzevVAzhs_80WZk2eLD3JeHwfekd1ddrbKUAeZN
'''
