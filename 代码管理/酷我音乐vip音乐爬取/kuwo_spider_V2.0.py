# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : kuwo_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/1 22:07
# ------------------------------
from requests_html import HTMLSession
from urllib.parse import quote
from jsonpath import jsonpath
from pprint import pprint
import os
session = HTMLSession()
'''
    http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%91%A8%E6%9D%B0%E4%BC%A6&pn=2&rn=30&httpsStatus=1&reqId=39ebd110-9373-11eb-8ebb-e907b7c7f3f8
    http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%91%A8%E6%9D%B0%E4%BC%A6&pn=3&rn=30&httpsStatus=1&reqId=55aaef80-9373-11eb-8ebb-e907b7c7f3f8
    http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E5%91%A8%E6%9D%B0%E4%BC%A6&pn=4&rn=30&httpsStatus=1&reqId=5d810230-9373-11eb-8ebb-e907b7c7f3f8
'''


class Kuwo_spider(object):
    # 1.url+headers
    def __init__(self):
        self.singer = input('请输入要下载歌曲的歌手名称：')
        self.singer_url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&httpsStatus=1&reqId=841eab11-92f4-11eb-8632-d5b34e4454c4'
        self.song_url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1617287325683&httpsStatus=1&reqId=841eab11-92f4-11eb-8632-d5b34e4454c4'
        self.headers = {
            # 存储用户信息  用户访问历史信息
            'Cookie': 'td_cookie=18446744073688118106; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1617285871; _ga=GA1.2.1836780651.1617285871; _gid=GA1.2.358485558.1617285871; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1617286417; kw_token=JIW4GG6XNC',
            # 钥匙
            'csrf': 'JIW4GG6XNC',
            # 告诉对方服务器，这一个请求来自于哪一个页面
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
            # 浏览器的标识
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        os.makedirs('./{}'.format(self.singer), exist_ok=True)


    # 2.解析歌手的url,获取歌手的歌曲
    def parse_singer_url(self):
        singer = quote(self.singer)
        pn = 1
        while True:
            response = session.get(self.singer_url.format(singer,pn),headers=self.headers)
            # pprint(response)
            if response.status_code != 200:
                break
            else:
                next_url_ids = jsonpath(response.json(), '$..rid')
                song_names = jsonpath(response.json(), '$..name')
                for next_url_id,song_name in zip(next_url_ids,song_names):
                    # print(song_name,song_url_id)
                    self.parse_song_url(next_url_id, song_name)
            pn += 1


    # 3.解析每首歌曲的url，获取歌曲下载链接
    def parse_song_url(self,next_url_id, song_name):
        next_url = self.song_url.format(next_url_id)
        response = session.get(next_url, headers=self.headers).json()
        # pprint(response)
        song_url = response['url']
        self.get_song_content(song_url,song_name)

    # 4.得到歌曲数据
    def get_song_content(self,song_url,song_name):
        song_content = session.get(song_url).content
        self.save_song_data(song_content,song_name)

    # 5.保存歌曲数据
    def save_song_data(self,song_content,song_name):
        try:
            with open('./{}/{}.m4a'.format(self.singer,song_name),'wb')as f:
                f.write(song_content)
                print('********歌曲：{}下载完成*********'.format(song_name))
        except Exception as e:
            print('歌曲保存失败：{}'.format(e))

    # 6.执行函数
    def main(self):
        self.parse_singer_url()

if __name__ == '__main__':
    song = Kuwo_spider()
    song.main()