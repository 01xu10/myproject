# !/usr/bin/env python
# -*- coding: utf-8 -*-
''''''

'''
    https://music.163.com/   网易云--静态网页
    
    http://music.163.com/song/media/outer/url?id=1471064193.mp3
    http://music.163.com/song/media/outer/url?id=1824927085.mp3
    http://music.163.com/song/media/outer/url?id=1450574147.mp3
    
    1、分析网页： 静态网页， 动态网页
        在网页源代码中，能够搜索到 网页所展示的部分！    --- 静态网页          静态加载
        在网页源代码中，不能够搜索到 网页所展示的部分！  --- 动态网页          动态加载  -- XHR data
        
'''

'''
    这里涉及到一个加密：
        http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
        
        {"errorCode":50}
        
        解决办法：_o  去掉！
        
        
        https://music.163.com/discover/toplist?id=3778678
        
        加密部分： #/
        
        Q:那怎么判断网址加密的符号是谁？一个一个试试吗？  写的多  经验！
        
        泡妞法则？一定是没有！
'''

import requests, os
from lxml import etree
from pprint import pprint

def main():
    # 1、url + headers
    start_url = 'https://music.163.com/#/discover/toplist?id=3778678'.replace('#/', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    # 2、请求数据，获取网页源代码
    response = requests.get(start_url, headers=headers).content.decode()
    # print(response)

    # 3、继续分析网页  复制703行   //: 定位整个网页源代码的任意位置  class="f-hide"
    html_xpath = etree.HTML(response)
    song_names = html_xpath.xpath(r'//ul[@class="f-hide"]/li/a/text()')
    # pprint(song_names)
    song_ids = html_xpath.xpath(r'//ul[@class="f-hide"]/li/a/@href')
    # pprint(song_ids)

    '''
        http://music.163.com/song/media/outer/song?id=1823305772.mp3
        http://music.163.com/song/media/outer/url?id=1450574147.mp3 网易云下载的接口
    '''

    # 4、循环遍历，得到 song_name, song_id   sep: 用来分割  一定是用print pprint
    for song_name, song_id in zip(song_names, song_ids):

        # 5、替换  song_id
        song_id = song_id.split('/song?')[1]
        # print(song_id)

        # 6、构造song_url
        song_url = 'http://music.163.com/song/media/outer/url?{}.mp3'.format(song_id)
        # print(song_url)

        # 7、获取song_content
        song_content = requests.get(song_url, headers=headers).content

        # 8、创建文件夹
        os.makedirs(r'./网易云音乐', exist_ok=True)

        # 9、保存数据
        try:
            with open(r'./{}/{}.mp3'.format('网易云音乐', song_name), 'wb') as f:
                f.write(song_content)
            print(r'***歌曲下载完成：{}.mp3'.format(song_name))
        except Exception as e:
            continue


if __name__ == '__main__':
    main()

















