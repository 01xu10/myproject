# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------


'''
    #我该怎么跟别人解释，我平时不是这样的……  https://v.douyin.com/J4QvAmw/ 复制此链接，打开抖音搜索，直接观看视频！
'''

import requests, re, jsonpath, os
from pprint import pprint

def main():
    # 1、url + headers(手机版)
    link = input('请输入要下载的抖音链接：')
    start_url = 'https' + re.findall(r'https(.*?) ', link)[0]
    # pprint(start_url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044207 Mobile '
                      'Safari/537.36 MicroMessenger/6.7.3.1340(0x26070332) NetType/4G Language/zh_CN Process/tools'
    }

    # 2、提取重定向后的url地址中的video_id
    resp_url = requests.get(start_url, headers=headers).url
    # pprint(resp_url)
    video_id = re.findall(r'video/(.*?)/', resp_url)[0]
    # pprint(video_id)

    # 3、提取数字后，字符串的拼接
    next_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'.format(video_id)
    # pprint(next_url)

    # 4、访问拼接后的url地址
    response = requests.get(next_url, headers=headers).json()
    # pprint(response)

    # 5、提取响应中的视频标题和视频url
    tik_tok_name = jsonpath.jsonpath(response, '$..desc')[0]
    # pprint(tik_tok_name)
    play_addr = jsonpath.jsonpath(response, '$..play_addr')[0]
    # pprint(play_addr)
    tik_tok_url_watermark = jsonpath.jsonpath(play_addr, '$..url_list')[0][0]
    # pprint(tik_tok_url_watermark)

    # 6、删除play后面的wm, 无水印视频需要用手机版访问
    tik_tok_url = tik_tok_url_watermark.replace('playwm', 'play')
    # pprint(tik_tok_url)

    # 7、发送抖音视频请求
    tik_tok_content = requests.get(tik_tok_url, headers=headers).content

    # 8、创建文件夹
    os.makedirs(r'./TikTok', exist_ok=True)

    # 9、保存数据
    try:
        with open(r'./TikTok/{}.mp4'.format(tik_tok_name), 'wb') as f:
            f.write(tik_tok_content)
    except Exception as e:
        print('***此抖音链接有错误...')


if __name__ == '__main__':
    main()