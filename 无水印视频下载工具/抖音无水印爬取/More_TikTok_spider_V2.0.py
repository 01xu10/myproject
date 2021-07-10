# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

"""
    用类去实现，抖音用主页视频的爬取
"""

'''
    https://www.iesdouyin.com/web/api/v2/aweme/post/?
    sec_uid=MS4wLjABAAAANh5LI7THTj_sMCbKMuLhf6Ho1o_wmzagjYSwSj_a5RI&count=21&
    max_cursor=0&
    aid=1128&
    _signature=KMR9HAAASOTAHl9hK6VqtCjEfQ&
    dytk=
'''

import re,requests,jsonpath,os
from pprint import pprint

class Tik_tok(object):

    # 1.初始url+headers,链接所需的参数
    def __init__(self, request_URL):
        self.headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36'
        }

        self.sec_uid = re.findall(r'sec_uid=(.*?)&',request_URL)[0]
        self.signature = re.findall(r'_signature=(.*?)&',request_URL)[0]
        self.max_cursor = 0
        self.num = 0
        self.video_num = 0

    # 2.对链接发请求,频繁请求，直到有数据为止
    def respone(self):
        print('*******正在请求抖音界面*******')
        while True:
            start_url = r'https://www.iesdouyin.com/web/api/v2/aweme/post/?' \
                        r'sec_uid={}&count=21&max_cursor={}&aid=1128&_signature={}&' \
                        r'dytk='.format(self.sec_uid, self.max_cursor, self.signature)
            self.num += 1
            respone = requests.get(start_url, headers=self.headers).json()
            # pprint(respone)
            aweme_list = jsonpath.jsonpath(respone, '$..aweme_list')[0]
            # 列表不为空则进行解析，通过判断has_more: true来进行翻页
            if aweme_list:
                print('--------------------------')
                print('*******第{}次请求成功*******'.format(self.num))
                has_more = jsonpath.jsonpath(respone, '$..has_more')[0]
                if has_more == True:
                    self.prase_data(respone)
                    print('*******第{}个视频下载完成*******'.format(self.video_num))
                    print('---------------------------')
                    print(' ')
                elif has_more == False:
                    self.prase_data(respone)
                    print('******已下载完作者所有视频,共{}个视频******'.format(self.video_num))
                    break
            else:
                continue


    # 3.解析数据，抖音视频链接在json数据中，用jsonpath解析数据,获取作者名称，视频名称，视频url，获取max_cursor的值
    def prase_data(self, respone):
        self.author_name = jsonpath.jsonpath(respone, '$..nickname')[0]
        # pprint(self.author_name)
        video_names = jsonpath.jsonpath(respone, '$..desc')
        # pprint(self.video_names)
        play_addr_lowbr = jsonpath.jsonpath(respone, '$..play_addr_lowbr')
        video_urls = jsonpath.jsonpath(play_addr_lowbr, '$..url_list')
        # pprint(self.video_urls)
        self.max_cursor = jsonpath.jsonpath(respone, '$..max_cursor')[0]
        # pprint(self.max_cursor)
        for video_name,video_url in zip(video_names,video_urls):
            self.save_content(video_name,video_url[0])

    # 4.保存数据
    def save_content(self, video_name,video_url):
        video_content = requests.get(video_url, headers=self.headers).content

        # 创建文件夹
        os.makedirs(r'./{}'.format(self.author_name), exist_ok=True)

        try:
            with open(r'./{}/{}.mp4'.format(self.author_name, video_name), 'wb') as f:
                f.write(video_content)
                print('****视频正在下载:{}'.format(video_name))
                self.video_num += 1

        except Exception as e:
            pass

    # 5.执行
    def main(self):
        self.respone()


if __name__ == '__main__':
    request_URL = input(r'请输入抖音的request_URL：')
    tiktok = Tik_tok(request_URL)
    tiktok.main()

'''
    https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAANh5LI7THTj_sMCbKMuLhf6Ho1o_wmzagjYSwSj_a5RI&count=21&max_cursor=0&aid=1128&_signature=KMR9HAAASOTAHl9hK6VqtCjEfQ&dytk=
'''