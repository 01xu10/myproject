# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : qidian_novel_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/6 12:44
# ------------------------------

from requests_html import HTMLSession
from pprint import pprint
from lxml import etree
from fake_useragent import UserAgent
import os
ua =UserAgent()
session = HTMLSession()

class Noval_spider(object):
    def __init__(self):
        self.title = input('请输入小说标题：')
        self.start_url = 'https://www.qidian.com/search?kw={}'.format(self.title)
        self.headers = {
            'upgrade-insecure-requests': '1',
            'cookie': '_yep_uuid=e4f4c0be-4444-493d-9346-7d40df587ab3; e1=%7B%22pid%22%3A%22qd_P_xiangqing%22%2C%22eid%22%3A%22qd_G55%22%2C%22l1%22%3A14%7D; e2=%7B%22pid%22%3A%22qd_P_xiangqing%22%2C%22eid%22%3A%22qd_G55%22%2C%22l1%22%3A14%7D; _csrfToken=044qpQVekj2tzP8g0kZKzHjGxTk1mE43pqdVU1AN; newstatisticUUID=1617682830_357569731; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; rcr=1735921; lrbc=1735921%7C30194132%7C1; e1=%7B%22pid%22%3A%22qd_P_Searchresult%22%2C%22eid%22%3A%22qd_S05%22%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_H_Search%22%2C%22l1%22%3A2%7D',
            'user-agent': ua.chrome
        }
        os.makedirs('./小说', exist_ok=True)

    def parse_start_url(self):
        response = session.get(self.start_url, headers=self.headers).content
        html_str = etree.HTML(response)
        novel_url = 'https:'+''.join(html_str.xpath('//*[@id="result-list"]/div/ul/li[1]/div[1]/a/@href'))
        # pprint(novel_url)
        novel_name = ''.join(html_str.xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h4/a/cite/text()'))
        if novel_name is '':
            novel_name = ''.join(html_str.xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h4/a/text()'))
        # pprint(novel_name)
        self.parse_novel_url(novel_url,novel_name)

    def parse_novel_url(self, novel_url,novel_name):
        '''
        解析小说主页链接，获取阅读文章的入口
        :param novel_url: 小说主页链接
        :return:
        '''
        response = session.get(novel_url, headers=self.headers).content
        html_str = etree.HTML(response)
        novel_start_url = 'https:' + ''.join(html_str.xpath('//a[@id="bookImg"]/@href'))
        # pprint(content_url)
        self.parse_nexr_url(novel_start_url,novel_name)

    def parse_nexr_url(self, novel_start_url, novel_name):
        '''
        下载小说章节内容，获取每一章的标题，以及每一章对应的内容，写入text文件，回调该函数
        :param novel_start_url:
        :return:
        '''
        response = session.get(novel_start_url, headers=self.headers).content
        # pprint(response.decode())
        html_str = etree.HTML(response)
        section_title = ''.join(html_str.xpath('//*[@class="text-wrap"]/div/div[@class="text-head"]/h3/span[1]/text()'))
        # print(section_title)
        with open('./小说/{}.text'.format(novel_name),'a+',encoding='UTF-8')as f:
            f.write(section_title + '\n\t')
        novel_content = '\n'.join(html_str.xpath('//div[@class="read-content j_readContent"]/p/text()'))
        # print(novel_content)
        with open('./小说/{}.text'.format(novel_name),'a+',encoding='UTF-8')as f:
            f.write(novel_content)
        # pprint(next_url)
        end = ''.join(html_str.xpath('//*[@id="j_chapterNext"]/text()'))
        # print(end)
        if end == '书末页':
            print('{}===已下载完成'.format(novel_name))
        else:
            next_url = 'https:' + ''.join(html_str.xpath('//*[@id="j_chapterNext"]/@href'))
            print('{}==={}====下载完成'.format(novel_name,section_title))
            self.parse_nexr_url(next_url, novel_name)


if __name__ == '__main__':
    noval = Noval_spider()
    noval.parse_start_url()