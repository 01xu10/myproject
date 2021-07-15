# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

import requests,parsel,pdfkit
from lxml import etree
from pprint import pprint


def main():
    # 1.url + headers
    start_url = input("请输入要下载的CSDN链接：")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2.发起请求
    respone = requests.get(start_url,headers=headers).text
    # pprint(respone)
    # 3.解析数据
    html_str = etree.HTML(respone)
    # 4.获取姓名，标题，html文本，用css选择器获取文本，不能用xpath
    article_title = html_str.xpath(r'//h1[@id="articleContentId"]/text()')[0]
    # print(author_name)
    author_name = html_str.xpath(r'//a[@id="uid"]/@title')[0]
    # print(author_name)
    html_content = parsel.Selector(respone)
    article_content = html_content.css('article').get()

    # 5.构造html内容
    html_new = \
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{}</title>
    </head>
    <body>
        {}
    </body>
    </html>
    """.format(article_title,article_content)

    # 6.把html内容写进html文件
    with open('./{}.html'.format(article_title),'w', encoding='utf-8') as f:
        f.write(html_new)
        # print("html页面保存成功：{}".format(article_title))

    # 7.把html文件转换为pdf
    try:
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file(r'{}.html'.format(article_title), r'{}.pdf'.format(article_title), configuration=config)
        print("文件下载成功：{}".format(article_title))
    except Exception as e :
        print("文件转换失败")

if __name__ == '__main__':
    main()