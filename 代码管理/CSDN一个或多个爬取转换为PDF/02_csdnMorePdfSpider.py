# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

'''
    测试url：https://blog.csdn.net/weixin_44145452    https://blog.csdn.net/weixin_48057068
'''

import requests, re, parsel, os, pdfkit
from lxml import etree
from pprint import pprint

def main():
    # 1、url + headers
    start_url = input('请输入博主的连接： ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36'
    }

    # 2、请求获取响应
    response = requests.get(start_url, headers=headers).text
    # pprint(response)

    # 3、解析数据   //:定位任意位置！
    html_xpath_1 = etree.HTML(response)
    boke_ids = html_xpath_1.xpath(r'//div[@class="article-item-box csdn-tracking-statistics"]/@data-articleid')
    # pprint(boke_ids)
    author_name = html_xpath_1.xpath(r'//a[@id="uid"]/@title')[0]
    # pprint(author_name)
    author_id = re.findall(r'https://blog.csdn.net/(.*?\d$)', start_url)[0]
    # print(author_id)

    # 4、遍历循环构造 博客的url
    for boke_id in boke_ids:
        boke_url = r'https://blog.csdn.net/{}/article/details/{}'.format(author_id, boke_id)

        # 5、发请求，得到boke_info
        boke_info = requests.get(boke_url, headers=headers).text

        # 6、解析数据：boke_name, boke_content:CSS选择器
        html_xpath_2 = etree.HTML(boke_info)
        boke_name = html_xpath_2.xpath('//h1[@id="articleContentId"]/text()')[0]
        # print(boke_name)
        html_css = parsel.Selector(boke_info)
        boke_content = html_css.css('article').get()

        # 7、拼接构造html页面
        html = \
            f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>首页</title>
                </head>
                <body>
                    {boke_content}
                </body>
                </html>
            '''

        # 8、创建html文件夹  pdf文件夹
        os.makedirs(r'{}-html'.format(author_name), exist_ok=True)
        os.makedirs(r'{}-pdf'.format(author_name), exist_ok=True)

        # 9、写html页面
        try:
            with open(r'{}-html/{}.html'.format(author_name, boke_name), 'w', encoding='utf-8') as f:
                f.write(html)
                # print(r'html文件保存成功：{}-html/{}.html'.format(author_name, boke_name))
        except Exception as e:
            continue

        # 10、文件的转换
        try:
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_file(
                r'{}-html/{}.html'.format(author_name, boke_name),
                r'{}-pdf/{}.pdf'.format(author_name, boke_name),
                configuration=config
            )
            print('文件正在下载：{}.pdf'.format(boke_name))
        except Exception as e:
            continue


if __name__ == '__main__':
    main()
