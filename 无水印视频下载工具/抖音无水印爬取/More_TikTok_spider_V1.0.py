# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

"""
   https://www.iesdouyin.com/web/api/v2/aweme/post/?
   sec_uid=MS4wLjABAAAAjoHZDBqJn14lTMqs9gAv7qrJ_OIHEu3Zkqaf3BWDHfIIeDCGCTkWs5yENOsDgr1y&
   max_cursor=0
   _signature=5qAZfQAAhsAOejsAGgH3o-agGW&dytk=
"""


import requests,re,jsonpath,os
from pprint import pprint
def main():
    # 1.url + headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Mobile Safari/537.36'
    }

    requests_url = input("请输入要请求的Request URL：")

    # 2.准备重定向链接的参数，sec_uid，max_cursor，signature
    sec_uid =re.findall(r'sec_uid=(.*?)&',requests_url)[0]
    signature =re.findall(r'_signature=(.*?)&',requests_url)[0]
    max_cursor = 0
    print('****正在请求抖音页面***' + '\n')

    # 2、循环请求，得到response, 设置num=0，统计请求次数
    num = 0
    while True:
        # start_url
        start_url = r'https://www.iesdouyin.com/web/api/v2/aweme/post/?' \
                    r'sec_uid={}&count=21&max_cursor={}' \
                    r'&aid=1128&_signature={}&dytk='.format(sec_uid,max_cursor,signature)
        requests.packages.urllib3.disable_warnings()
        reponse = requests.get(start_url, headers=headers, verify=False).json()
        aweme_list = jsonpath.jsonpath(reponse, '$..aweme_list')[0]

        # 3、如果请求到数据，则解析数据
        if aweme_list:
            print('***第{}次请求成功***'.format(num+1))
            pprint(aweme_list)
            # 3、解析得到video_names, video_urls, author_name
            author_name = jsonpath.jsonpath(response, '$..nickname')[0]
            video_names = jsonpath.jsonpath(response, '$..desc')
            play_addr_lowbr = jsonpath.jsonpath(response, '$..play_addr_lowbr')
            video_urls = jsonpath.jsonpath(play_addr_lowbr, '$..url_list')
            max_cursor = jsonpath.jsonpath(response, '$..max_cursor')[0]


            # 4、循环遍历得到video_name, video_url, 请求video_url,
            for video_name, video_url in zip(video_names, video_urls):
                try:
                    video_content = requests.get(video_url[0], headers=headers).content
                except Exception as e:
                    continue

                # 5、创建文件夹
                if not os.path.exists(r'./{}'.format(author_name)):
                    os.mkdir(r'./{}'.format(author_name))

                # 6、保存文件
                try:
                    with open(r'./{}/{}.mp4'.format(author_name, video_name), 'wb') as f:
                        f.write(video_content)
                        print('***视频正在下载：{}.mp4***'.format(video_name))
                except Exception as e:

               print('***此视频不可下载***')
            print('----------------------------------------------------------' + '\n')



        num += 1

if __name__ == '__main__':
    main()