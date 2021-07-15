# !/usr/bin/env python
# -*- coding: utf-8 -*-


import requests, jsonpath, os
from pprint import pprint


def main():
    # 1、url + headers
    key = input('请输入要下载的歌手的名字：')

    start_url = 'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key={}' \
                '&pn=1&rn=30&httpsStatus=1&reqId=870a0ab0-39dd-11eb-afa8-afc209acddcc'.format(key)

    player_url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=16' \
               '07492189696&httpsStatus=1&reqId=7cf74710-39e0-11eb-a3e8-49c2dda7238f'

    headers = {
        'Cookie': '_ga=GA1.2.610256576.1607490904; _gid=GA1.2.1433999021.1607490904; Hm_lvt_cdb524f42f0ce19b169a807112'
                  '3a4797=1607490903,1607492134; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1607492134; kw_token=USI22KJF9IL',
        'csrf': 'USI22KJF9IL',
        'Host': 'www.kuwo.cn',
        'Referer': 'https://kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2、发送请求
    response = requests.get(start_url, headers=headers).json()
    # pprint(response)

    # 3、解析数据
    # 获取歌曲名
    song_name_list = jsonpath.jsonpath(response, '$..name')
    # print(song_name_list)
    # 获取rid
    song_rid_list = jsonpath.jsonpath(response, '$..rid')
    # print(song_rid_list)

    for song_name, rid in zip(song_name_list, song_rid_list):
        song_url_json = requests.get(player_url.format(rid), headers=headers).json()
        # pprint(song_url_json)
        song_url = jsonpath.jsonpath(song_url_json, '$..url')[0]
        # pprint(song_url)
        song_content = requests.get(song_url).content

        # 4、创建文件夹
        try:
            os.makedirs('./{}'.format(key), exist_ok=True)

            # 5、保存歌曲
            with open('./{}/{}.mp3'.format(key, song_name), 'wb') as f:
                print('***{}.mp3***正在下载！'.format(song_name))
                f.write(song_content)

        except Exception as e:
            print('下载错误')


if __name__ == '__main__':
    main()