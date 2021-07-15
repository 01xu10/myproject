# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : weibo_comment_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/5 15:18
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from pprint import pprint
from xlutils.copy import copy
from urllib.parse import quote
from lxml import etree
import os,re,jsonpath,time,xlwt, xlrd
ua = UserAgent()
session = HTMLSession()

class weibo_conmment(object):
    # 1.url+headers
    def __init__(self):
        self.title = input('请输入明星微博id（周杰伦）：')
        self.start_url = 'https://s.weibo.com/weibo/{}'
        self.headers = {
            'Cookie': 'SINAGLOBAL=6886286721179.622.1608355841235; wb_timefeed_6483602047=1; wb_view_log_6483602047=1536*8641.25; SCF=AhwH7DgXcfRCAeG5h25bpgzoj1aIBNJh4818e7cNFXKBOBuw3lLmgWuw3Xm48BhEyGbsHCxhVTBv3nIFOSUVA6o.; wb_view_log=1536*8641.25; SUB=_2A25Na7s3DeThGeNG4lAV-S7FzziIHXVul8V_rDV8PUJbkNAKLVrEkW1NSunjMyzdFWWgRa8tWMuwLkDM-L-Dl0M8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF77BzRp2TupZOvubAGO80s5NHD95Qf1h.ESh.71KBXWs4DqcjGeK8gKgSXd7tt; wvr=6; wb_view_log_5892490944=1536*8641.25; _s_tentry=www.baidu.com; UOR=,,www.baidu.com; Apache=1056311703742.2831.1617966071034; ULV=1617966071039:15:12:8:1056311703742.2831.1617966071034:1617939196887; webim_unReadCount=%7B%22time%22%3A1617966282953%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A7%2C%22msgbox%22%3A0%7D',          'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.chrome
        }
        self.num = 0
    # 2.从微博主页中输入明星名称，获取微博主页url
    def parse_url_response(self):
        title = quote(self.title)
        start_url = self.start_url.format(title)
        resp = session.get(start_url,headers=self.headers)
        # pprint(resp.html.html)
        wb_url = 'https:'+''.join(resp.html.xpath('//*[@id="pl_feedlist_index"]/div[1]/div[1]/div/div[2]/div/a[1]/@href'))
        # pprint(wb_url)
        self.parse_zy_url_response(wb_url,title)


    def parse_zy_url_response(self, wb_url,title):
        '''
        解析用户微博主页url,解析该页面，获取每个微博的id
        :param wb_url: 微博主页的url
        :return:
        '''
        time.sleep(2)
        print('******正在进入{}微博主页*******'.format(self.title))
        response = session.get(wb_url, headers=self.headers).content.decode().replace('\\','')
        # print(response)
        wb_mids = re.findall('mid="(.*?)"',response)
        # pprint(wb_ids)
        for wb_mid in wb_mids:
            self.parse_wb_comment_url(wb_mid)
            break
    '''
        https://m.weibo.cn/comments/hotflow?id=4609364540787337&mid=4609364540787337&max_id_type=0
        https://m.weibo.cn/comments/hotflow?id=4609364540787337&mid=4609364540787337&max_id=1734103859794300&max_id_type=0
    '''

    def parse_wb_comment_url(self, wb_mid, next_url=None, max_id=None):
        '''
        根据获取到的mid构造第一个requests_url,通过手机端的ua获取评论内容，再从第一个requesrts_url中找翻页的max_id
        手机端的需要构造新headers,从手机端页面中分析，观察referer的规律，发现都是来自微博正文的地址，可使用固定referer
        :param wb_mid: 构造requests_url
        :return:
        '''
        time.sleep(3)
        print('*******正在获取评论信息********')
        if next_url is None:
            next_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(wb_mid, wb_mid)
        else:
            next_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(wb_mid, wb_mid, max_id)
        headers = {
            'Cookie': '_T_WM=32239906866; SCF=AhwH7DgXcfRCAeG5h25bpgzoj1aIBNJh4818e7cNFXKBBmuv8Hk4T_5VtJY85DFJF3VFaKlJ2aEMU_Zs4eLugx8.; SUB=_2A25Na7s4DeThGeNG4lAV-S7FzziIHXVul8VwrDV6PUJbktANLULkkW1NSunjM08Pumz8ya0fH7P_5gEbHg6jQ7ZM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF77BzRp2TupZOvubAGO80s5NHD95Qf1h.ESh.71KBXWs4DqcjGeK8gKgSXd7tt; XSRF-TOKEN=69df98; WEIBOCN_FROM=1110005030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000061%26fid%3D4599795782255447%26oid%3D4599795782255447',        'referer': 'https://m.weibo.cn/status/' + str(wb_mid),
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': 'ebe7af'
        }
        # print(next_url)
        response = session.get(next_url, headers=headers)
        # print(response.json())
        max_id =jsonpath.jsonpath(response.json(), '$..max_id')[0]
        # print(max_id)
        self.parse_comment_data(response.json())
        # 回调函数
        self.parse_wb_comment_url(wb_mid, next_url=next_url, max_id=max_id)


    def parse_comment_data(self, response):
        comment_list = response['data']['data']
        for comment in comment_list:
            # 评论内容
            time.sleep(0.2)
            text = jsonpath.jsonpath(comment,'$..text')[0]
            if 'span' in text:
                text = re.sub('<span.*?</span>',''.join(re.findall('alt=(.*?)',text)),text)
            if '</a>' in text:
                text = re.sub('<a.*?</a>', ''.join(re.findall('>(.*?)</a>', text)), text)

            # 用户id
            user_id = comment['user']['id']
            # 用户名
            user_name = jsonpath.jsonpath(comment,  '$..screen_name')[0]
            self.num += 1
            print('=========第{}条评论下载完成======='.format(self.num))
            # print(user_name,user_id,text)
            list_1 = [user_name,user_id,text]
            dict_1 = {'微博评论': list_1}
            self.save_excel(dict_1)

    def save_excel(self, data):
        # data = {
        #     '基本详情': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        # }
        os_path_1 = os.getcwd() + '/微博评论数据/'
        os.makedirs(os_path_1, exist_ok=True)
        # os_path = os_path_1 + self.os_path_name + '.xls'
        os_path = os_path_1 + f'{self.title}微博评论.xls'
        if not os.path.exists(os_path):
            # 创建新的workbook（其实就是创建新的excel）
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建新的sheet表
            worksheet1 = workbook.add_sheet("微博评论", cell_overwrite_ok=True)
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
            excel_data_1 = ('粉丝昵称','粉丝id', '评论内容')
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




    def main(self):
        self.parse_url_response()

if __name__ == '__main__':
    comment = weibo_conmment()
    comment.main()