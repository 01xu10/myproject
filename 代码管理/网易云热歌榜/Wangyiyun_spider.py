# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : Wangyiyun_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/3/18 15:40
# ------------------------------

import requests,os
from lxml import etree
from pprint import pprint

class Hot_music(object):
    # 1.url+header
    def __init__(self):
        self.start_url = 'https://music.163.com/#/discover/toplist?id=3778678'.replace('#/', '')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

    # 2.解析页面
    def response(self):
        response = requests.get(self.start_url,headers=self.headers).text
        # pprint(response)
        self.analysis_data(response)

    # 3.获取歌曲的id，名称，构造歌曲下载的url
    def analysis_data(self,response):
        html_xpath = etree.HTML(response)
        song_ids = html_xpath.xpath(r'//ul[@class="f-hide"]/li/a/@href')
        # pprint(song_ids)
        song_names = html_xpath.xpath(r'//ul[@class="f-hide"]/li/a/text()')
        # pprint(song_names)
        for song_id,song_name in zip(song_ids,song_names):
            song_id = song_id.split('/song?')[1]
            song_url = 'http://music.163.com/song/media/outer/url?{}.mp3'.format(song_id)
            song_content = requests.get(song_url, headers=self.headers).content
            self.save_data(song_content,song_name)


    # 4. 保存数据
    def save_data(self,song_content,song_name):
        # 创建文件夹
        os.makedirs(r'./网易云音乐', exist_ok=True)

        # 保存数据
        try:
            with open(r'./{}/{}.mp3'.format('网易云音乐', song_name),'wb')as f:
                f.write(song_content)
            print('{}.mp3下载完成'.format(song_name))
        except Exception as e:
            print('{}.mp3下载失败'.format(song_name))
    # 5.执行代码
    def main(self):
        self.response()


if __name__ == '__main__':
    music =Hot_music()
    music.main()