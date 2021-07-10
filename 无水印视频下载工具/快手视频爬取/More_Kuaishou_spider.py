# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : More_Kuaishou_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/26 14:16
# ------------------------------
import requests,json,jsonpath,os,re,time
from pprint import pprint

class More_Kuaishou_video(object):
    # 1.url+headers
    def __init__(self):
        self.url_1 = input('请输入快手博主主页的分享链接：')
        self.request_url_1 = 'https://live.kuaishou.com/m_graphql'
        self.request_url_2 = 'https://video.kuaishou.com/graphql'
        # 注意请求头加上content-type，因为太多个包请求不到数据，所以添加上cookie
        self.headers_1 = {
            'Content-Type': 'application/json',
            'Cookie': 'did=web_14673a8dc2ae4bc2a17d7cd9d74cdb53; didv=1614141080000; clientid=3; client_key=65890b29; kpn=GAME_ZONE; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1614141196; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; userId=42440705; userId=42440705; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAW71rkV0LMlnCjNZ5DfElTEysP_OFI_4dm6Nop1mLIbeIVgvuSY93r_IvsuabLIghV_ZWyLh3xWG6CuoXHNriQret0FO4JG9CQ_wmcdhukX67S2WifdtvPr_xBtxkLINiVuDT5aasJW__v8_ijmA8XCD1YUlPCjpVBUOjt67RqzWuDBhvG5VBKPKxOhigSZm8lCsNdlQN_2KM_XaMkF6ENMaEgCrAu8bFEUPixNgRvVq1Nb0ZSIgUWZMAFThAtQYOSCU8cn_efGABwtKipmJI8r3Y2ZDnRMoBTAB; kuaishou.live.web_ph=22cd96a12afdf5bfa3602ac2d3cd1407acdf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/88.0.4324.190 Safari/537.36'
        }
        # 注意请求头加上content-type
        self.headers_2 = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        # 翻页符
        self.page_turning = ""
        # 计数器
        self.a = 0
        self.num = 0
        # 获取快手博主id
        self.start_url_1 = re.findall('https:.*? ',self.url_1)[0]
        self.start_url = requests.get(self.start_url_1,headers=self.headers_1).url
        # print(self.start_url)
        self.user_id = re.findall('profile/(.*?)?fid',self.start_url)[0].replace('?','')
        # print(self.user_id)


    # 2.解析数据
    def first_parse(self):
        while True:
            play_load_1 = {"operationName": "publicFeedsQuery","variables": {"principalId": "", "pcursor": "", "count": 24},"query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}
            play_load_1["variables"]["pcursor"] = self.page_turning
            play_load_1["variables"]["principalId"] = self.user_id
            # 这里是字典转成json字符串 因为payload参数接受的json格式的 不是字典格式的
            play_load = json.dumps(play_load_1)
            # post请求，并且需要传递payload参数
            respone = requests.post(url=self.request_url_1, headers=self.headers_1, data=play_load).json()
            # 获取翻页标志
            self.page_turning = jsonpath.jsonpath(respone, '$..pcursor')[0]
            # 判断是否可以翻页
            if play_load_1["variables"]["pcursor"] != "no_more":
                self.user_name = respone['data']['publicFeeds']['list'][0]['user']['name']
                for i in range(0, len(respone['data']['publicFeeds']['list'])):
                    video_id = respone['data']['publicFeeds']['list'][i]['id']
                    # pprint(video_id)
                    self.get_video_id(video_id)

            else:
                for i in range(0, len(respone['data']['publicFeeds']['list'])):
                    video_id = respone['data']['publicFeeds']['list'][i]['id']
                    # pprint(video_id)
                    self.get_video_id(video_id)
                break
        print('已下载完成作者所有作品，共{}个视频'.format(self.num))

    # 3.获取视频id
    def get_video_id(self, video_id):
        payload_2 = {"operationName": "visionVideoDetail", "variables": {"photoId": "", "page": "detail"},
                     "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    __typename\n  }\n}\n"}
        payload_2["variables"]["photoId"] = video_id
        # 这里是字典转成json字符串 因为payload参数接受的json格式的 不是字典格式的
        payload = json.dumps(payload_2)
        self.prase_data(payload)

    # 4.获取视频url，和视频名称
    def prase_data(self, payload):
        # post请求，并且需要传递payload参数
        while True:
            respone = requests.post(url=self.request_url_2, headers=self.headers_2, data=payload).json()
            # pprint(respone)
            # 有时候会出现请求失败，返回空json数据
            if respone['data']['visionVideoDetail']:
                # 避免遇到博主作品放置图片
                try:
                    self.num += 1
                    video_url = jsonpath.jsonpath(respone, '$..photoUrl')[0]
                    video_name = jsonpath.jsonpath(respone, '$..caption')[0]
                    # pprint(video_name)
                    # pprint(video_url)
                    self.save_video(video_url, video_name)
                    break
                except Exception as e:
                    print('下载错误，下载目标是图片集合')
                    break
            else:
                self.a +=1
                print("请求失败,第{}次重新请求".format(self.a))
                continue

    # 5.保存数据
    def save_video(self, video_url, video_name):
        video_content = requests.get(video_url, headers=self.headers_2).content
        # 创建问价夹
        os.makedirs('./{}'.format(self.user_name), exist_ok=True)
        # 保存视频
        try:
            with open('./{}/{}.mp4'.format(self.user_name,video_name), 'wb') as f:
                f.write(video_content)
                print('*******正在下载第{}个视频：{}*******'.format(self.num, video_name))
        except Exception as e:
            print('视频保存失败')

    # 6.执行代码
    def main(self):
        self.first_parse()

if __name__ == '__main__':
    kuaishou_videos = More_Kuaishou_video()
    # kuaishou_videos.main()