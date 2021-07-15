# !/usr/bin/env python
# -*- coding: utf-8 -*-
''''''

import requests, os
from lxml import etree
from pprint import pprint

def main():
    # 1、url + header
    for i in range(1, 230):
        start_url = r'https://ibaotu.com/shipin/7-0-0-0-0-{}.html'.format(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36'
        }

        # 2、发请求，获取响应
        response = requests.get(start_url, headers=headers).content.decode()
        # pprint(response)

        # 3、解析数据 得到 player_urls
        html_str = etree.HTML(response)
        video_names = html_str.xpath(r'//img[@class="scrollLoading"]/@alt')
        # print(video_names)
        player_urls = html_str.xpath(r'//a[@class="shade-box"]/@href')
        # pprint(player_urls)

        # 4、遍历发第二次请求
        for video_name, player_url in zip(video_names, player_urls):
            player_url = 'https:' + player_url
            response = requests.get(player_url, headers=headers).content.decode()
            # pprint(response)

            # 5、数据解析，得到video_urls, 并且发请求
            player_urls_str = etree.HTML(response)
            video_url = 'https:' + player_urls_str.xpath(r'//div[@class="img-wrap video-player-box"]/a/@src')[0]
            # pprint(video_url)
            video_content = requests.get(video_url, headers=headers).content
            # pprint(video_content)

            # 6、创建文件夹
            os.makedirs(r'./{}'.format('包图网视频'), exist_ok=True)

            # 7、保存文件
            try:
                with open(r'./{}/{}.mp4'.format('包图网视频', video_name), 'wb') as f:
                    print(r'***视频正在下载：{}.mp4'.format(video_name))
                    f.write(video_content)
            except Exception as e:
                print(r'***视频下载错误***')


if __name__ == '__main__':
    main()
