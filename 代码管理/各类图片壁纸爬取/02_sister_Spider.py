# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------


import requests, shutil, os
from lxml import etree
from pprint import pprint


def main():
    ''' 抓取小姐姐 '''
    # 1、url + headers
    for i in range(2, 259):
        start_url = 'https://www.mzitu.com/page/{}/'.format(i)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36',
            'referer': 'https://www.mzitu.com/xinggan/'
        }

        # 2、发送请求
        response = requests.get(start_url, headers=headers).content.decode()
        # pprint(response)

        # 3、解析数据
        html_str = etree.HTML(response)
        img_urls = html_str.xpath(r'//img[@class="lazy"]/@data-original')
        # pprint(img_urls)
        img_names = html_str.xpath(r'//img[@class="lazy"]/@alt')
        # pprint(img_names)

        for img_url, img_name in zip(img_urls, img_names):
            img_resp = requests.get(img_url, headers=headers).content
            os.makedirs('./image', exist_ok=True)
            try:
                with open(r'./image/{}.jpg'.format(img_name), 'wb') as f:
                    print('正在下载：***{}***'.format(img_name))
                    f.write(img_resp)
            except Exception as e:
                print('这个女人不能看...')


def delet():
    ''' 删除小姐姐 '''
    shutil.rmtree(r'./image')
    os.mkdir(r'./image')


if __name__ == '__main__':
    main()
    # delet()