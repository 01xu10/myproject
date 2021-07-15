# !/usr/bin/env python
# -*- coding: utf-8 -*-


import requests, os
from lxml import etree
from pprint import pprint


def main():
    # 1、url + headers
    for i in range(100):
        start_url = r'http://pic.netbian.com/e/search/result/index.php?page={}&searchid=16'.format(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36'
        }

        # 2、请求获取响应
        response = requests.get(start_url, headers=headers).content.decode('gbk')
        # pprint(response)

        # 3 解析数据
        html_str = etree.HTML(response)
        img_info_urls = html_str.xpath(r'//ul[@class="clearfix"]/li/a/@href')
        # pprint(img_info_urls)

        # 4、循环遍历 构造img_info_url
        for img_info_url in img_info_urls:
            img_info_url = 'http://pic.netbian.com' + img_info_url
            # print(img_info_url)

            # 5、对img_info_url发请求，解析得到img_urls
            response = requests.get(img_info_url, headers=headers).content.decode('gbk')
            html_str = etree.HTML(response)
            img_url = 'http://pic.netbian.com' + html_str.xpath(r'//a[@id="img"]/img/@src')[0]
            # pprint(img_url)
            img_name = html_str.xpath(r'//a[@id="img"]/img/@title')[0]
            # pprint(img_name)

            # 6、对img_url 请求 得到img_content
            img_content = requests.get(img_url, headers=headers).content

            # 7、创建文件夹
            os.makedirs('./{}'.format('image'), exist_ok=True)

            # 8、保存图片
            try:
                with open(r'./{}/{}.jpg'.format('image', img_name), 'wb') as f:
                    f.write(img_content)
                    pprint(r'**图片已下载： {}.jpg'.format(img_name))
            except Exception as e:
                continue


if __name__ == '__main__':
    main()
