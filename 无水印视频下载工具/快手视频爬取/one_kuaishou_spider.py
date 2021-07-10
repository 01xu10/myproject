# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : one_kuaishou_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/24 15:05
# ------------------------------

import requests,json,jsonpath,os,re
from pprint import pprint
from lxml import etree


class Kuaishou_spider(object):
    # 1.url+headers+data
    def __init__(self,start_url):
        self.id = re.findall(r'short-video/(.*?)?fid',start_url)[0].replace('?','')
        self.request_url = 'https://video.kuaishou.com/graphql'
        # 注意请求头加上content-type
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }

        # post请求，并且需要传递payload参数
        self.payload_1 = {"operationName":"visionVideoDetail","variables":{"photoId":"","page":"detail"},"query":"query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    __typename\n  }\n}\n"}
        self.payload_1["variables"]["photoId"]=self.id
        # 这里是字典转成json字符串 因为payload参数接受的json格式的 不是字典格式的
        self.payload = json.dumps(self.payload_1)



    # 2.解析数据
    def first_prase(self):
        respone = requests.post(url=self.request_url,headers=self.headers,data=self.payload).json()
        # pprint(respone)
        video_url = jsonpath.jsonpath(respone,'$..photoUrl')[0]
        video_name = jsonpath.jsonpath(respone,'$..caption')[0]
        # pprint(video_name)
        # pprint(video_url)
        self.save_video(video_url,video_name)

    # 3.保存数据
    def save_video(self,video_url,video_name):
        video_content = requests.get(video_url,headers=self.headers).content
        os.makedirs('./kuaishou_video',exist_ok=True)
        try:
            with open('./kuaishou_video/{}.mp4'.format(video_name),'wb') as f:
                f.write(video_content)
                print('*******正在下载{}*******'.format(video_name))
        except Exception as e:
            print('视频保存失败')


    # 4.执行代码
    def main(self):
        self.first_prase()

if __name__ == '__main__':
    start_url = input('请输入需要下载快手视频的长链接：')
    kuaishou = Kuaishou_spider(start_url)
    kuaishou.main()
