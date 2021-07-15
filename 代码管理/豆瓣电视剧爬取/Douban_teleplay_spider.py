# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : Douban_teleplay_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/3/27 23:55
# ------------------------------
import requests,random,re,time
from openpyxl import Workbook
from lxml import etree
from pprint import pprint
'''
    'Request URL: https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=40'
    'Request URL: https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=20'
    'Request URL: https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start=0'
'''
class Douban_teleplay_spider(object):
    def __init__(self):
        self.tag_url = 'https://movie.douban.com/j/search_tags?type=tv&tag=%E7%BE%8E%E5%89%A7&source='
        self.start_teleplay_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag={}&sort=recommend&page_limit=20&page_start={}'

        self.USER_AGENT = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2']
        self.headers = {
            'Referer': 'https://movie.douban.com',
            'User-Agent': random.choice(self.USER_AGENT)
        }
        self.number = 0
        self.wb = Workbook()
        self.wb.remove(self.wb['Sheet'])


    def tag_request(self):
        response = requests.get(self.tag_url, headers=self.headers).json()
        # pprint(response)
        url_tags = response['tags']
        # pprint(url_tags)
        for tag in url_tags:
            self.wb.create_sheet(title=tag)
            self.sheet = self.wb[tag]
            self.sheet.append(['电视剧', '评分', '类型', '制片国家/地区', '语言', '最新消息', '集数','时长', '首播','导演','编导','主演'])
            self.next_page(tag)
            self.number = 0
            print('')

    def next_page(self, tag):
        i = 0
        while True:
            tv_url = self.start_teleplay_url.format(tag, i)
            # pprint(tv_url)
            response = requests.get(tv_url, headers=self.headers).json()
            # pprint(response)
            # if response.status_code != 200:
            if i >= 20:
                break
            else:
                """当后续的代码操作报错，则终止这个while死循环
                程序，会回到上一个函数for位置，继续遍历，执行下一个电视剧分类的解析
                """
                try:
                    self.teleplay_request(response, tag)
                    # print(111)
                except:
                    break
            i += 20

    def teleplay_request(self,response,tag):
        tv_infos = response['subjects']
        # pprint(tv_infos)
        for tv_info in tv_infos:
            tv_title = tv_info['title']
            tv_url = tv_info['url']
            tv_score = tv_info['rate']
            tv_latest = tv_info['episodes_info']
            self.parse_data(tv_url,tv_title,tv_score,tv_latest,tag)

    def parse_data(self,tv_url,tv_title,tv_score,tv_latest,tag):
        response = requests.get(tv_url,headers=self.headers).text
        # pprint(response)
        html_str = etree.HTML(response)
        tv_director = ','.join(html_str.xpath('//*[@id="info"]/span[1]/span[2]/a/text()'))
        # pprint(tv_director)
        tv_writer = ','.join(html_str.xpath('//*[@id="info"]/span[2]/span[2]/a/text()'))
        # pprint(tv_writer)
        tv_actors = ','.join(re.findall('rel="v:starring">(.*?)</a>',response))
        # pprint(type(tv_actors))
        tv_type = ','.join(re.findall('<span property="v:genre">(.*?)</span>',response))
        # pprint(tv_type)
        tv_area = ''.join(re.findall('制片国家/地区:</span> (.*?)<br/>\\n',response))
        # pprint(tv_area)
        tv_language = ''.join(re.findall('语言:</span> (.*?)<br/>\\n',response))
        # pprint(tv_language)
        tv_first_show = ''.join(re.findall('首播:</span> <span property="v:initialReleaseDate" content="(.*?)">',response))
        # pprint(tv_first_show)
        tv_num = ''.join(re.findall('集数:</span> (.*?)<br/>\\n', response))

        tv_time = ''.join(re.findall('单集片长:</span> (.*?)<br/>\\n', response))
        # pprint(tv_time)
        self.number += 1
        self.save_teleplay_info(tv_title, tv_score, tv_type, tv_area, tv_language,  tv_latest, tv_num, tv_time,
                                tv_first_show, tv_director, tv_writer, tv_actors, tag)

    def save_teleplay_info(self,tv_title,tv_score,tv_type,tv_area,tv_language,tv_latest, tv_num, tv_time,tv_first_show,tv_director,tv_writer,tv_actors,tag):
        time.sleep(1)
        self.sheet.append([tv_title,tv_score,tv_type,tv_area,tv_language,tv_latest,tv_num, tv_time,tv_first_show,tv_director,tv_writer,tv_actors])
        print('\r***正在下载*** 栏目：{}， 电视剧信息：{}条***'.format(tag,self.number), end='')

    def main(self):
        self.tag_request()
        self.wb.save('douban_TV_info.xlsx')


if __name__ == '__main__':
    douban = Douban_teleplay_spider()
    douban.main()