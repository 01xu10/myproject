# !/usr/bin/env python
# -*- coding: utf-8 -*-
''''''

import requests
from lxml import etree
from pprint import pprint

def main():
    # 1、url + headers
    start_url = r'http://m.uustv.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2、form_data
    key = input(r'请输入名字：')
    form_data = {
        'word': key,
        'sizes': 60,
        'fonts': 'yqk.ttf',
        'fontcolor':  '# 000000'
    }

    # 3、请求数据
    response = requests.post(start_url, headers=headers, data=form_data).content.decode()
    # pprint(response)

    # 4、解析得到签名后的图片  先把响应变成xpath对象 xpath结果 是一个列表！
    # 定位到任意位置用： //
    # 获取属性用@    获取文本用text()
    html_str = etree.HTML(response)
    img_url = html_str.xpath('//div[@class="tu"]/img/@src')[0]
    img_url = start_url + img_url
    # pprint(img_url)

    # 5、对图片进行请求，得到图片的二进制数据
    img_content = requests.get(img_url, headers=headers).content

    # 6、保存数
    with open(r'{}.jpg'.format(key), 'wb') as f:
        f.write(img_content)
        print(r'签名照已生成：{}.jpg'.format(key))


if __name__ == '__main__':
    main()