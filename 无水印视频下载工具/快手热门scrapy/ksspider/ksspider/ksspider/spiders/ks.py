# -*- coding: utf-8 -*-
import scrapy, json


class KsSpider(scrapy.Spider):
    name = 'ks'
    allowed_domains = ['kuaishou.com']
    start_urls = ['https://video.kuaishou.com/graphql']

    def start_requests(self):
        # GET请求发送
        # yield scrapy.Request
        for i in range(20):
            headers = {
                'content-type': 'application/json',
                'Cookie': 'clientid=3; did=web_d8ccc186d82b7f7b61768498067e7f64; client_key=65890b29; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1600780303; kpf=PC_WEB; kpn=KUAISHOU_VISION; didv=1619528445000',
                'Host': 'video.kuaishou.com',
                'Origin': 'https://video.kuaishou.com',
                'Referer': 'https://video.kuaishou.com/brilliant',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
            data = {"operationName": "brilliantTypeDataQuery", "variables": {"hotChannelId": "00", "page": "brilliant"},
                    "query": "fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}

            # yield scrapy.FormRequest(
            #     url=self.start_urls[0],
            #     headers=headers,
            #     formdata=json.dumps(data),
            #     callback=self.parse
            # )
            yield scrapy.Request(
                url=self.start_urls[0],
                headers=headers,
                method='POST',
                body=json.dumps(data)
            )

    def parse(self, response):
        json_data = json.loads(response.body.decode())
        """取出视频信息大列表"""
        big_list = json_data['data']['brilliantTypeData']['feeds']
        """遍历大列表"""
        for data_dict in big_list:
            mp4_url = data_dict['photo']['photoUrl']
            mp4_name = data_dict['photo']['caption']
            yield scrapy.Request(
                url=mp4_url,
                callback=self.parse_mp4_data,
                meta={'title': mp4_name},
                dont_filter=True
            )

    def parse_mp4_data(self, response):
        """构造返回字典"""
        item = {}
        """获取视频的名称"""
        title = response.meta['title']
        item['title'] = title
        """视频的二进制数据"""
        data = response.body
        item['data'] = data
        yield item








