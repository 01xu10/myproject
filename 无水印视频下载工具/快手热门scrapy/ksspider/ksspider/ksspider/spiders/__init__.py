# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy import cmdline

cmdline.execute('scrapy crawl ks --nolog'.split(' '))



# from requests_html import HTMLSession
# from fake_useragent import UserAgent
# import json
# ua = UserAgent()
# session = HTMLSession()
#
#
# start_url = 'https://video.kuaishou.com/graphql'
# headers = {
#     'content-type': 'application/json',
#     'Cookie': 'clientid=3; did=web_d8ccc186d82b7f7b61768498067e7f64; client_key=65890b29; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1600780303; kpf=PC_WEB; kpn=KUAISHOU_VISION; didv=1619528445000',
#     'Host': 'video.kuaishou.com',
#     'Origin': 'https://video.kuaishou.com',
#     'Referer': 'https://video.kuaishou.com/brilliant',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
# }
# data = {"operationName": "brilliantTypeDataQuery", "variables": {"hotChannelId": "00", "page": "brilliant"},
#         "query": "fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}
# respone = session.post(start_url, headers=headers, data=json.dumps(data)).json()
# print(respone)












