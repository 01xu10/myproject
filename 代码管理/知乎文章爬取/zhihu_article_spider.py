# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : zhihu_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/2/8 15:05
# ------------------------------
import requests,parsel,pdfkit,re
from lxml import etree
from pprint import pprint

class Zhihu_Spider(object):
    # 1.url+headers
    def __init__(self, url):
        self.start_url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
    # 2.发起请求
    def request(self):
        respone = requests.get(self.start_url,headers=self.headers).text
        self.prase_data(respone)

    # 3.解析数据，获取标题，作者，文章
    def prase_data(self,respone):
        html_str = etree.HTML(respone)
        author_name = html_str.xpath(r'//*[@id="root"]/div/main/div/article/header/div[1]/div/meta[1]/@content')[0]
        # print(author_name)
        article_title = html_str.xpath(r'//*[@id="root"]/div/main/div/article/header/h1/text()')[0]
        # print(article_title)
        html_content = parsel.Selector(respone)
        article_content = html_content.css('#root > div > main > div > article > div.Post-RichTextContainer > div').get()
        article_content = re.sub(r'<noscript>|</noscript>.*?jpg">', '', article_content)
        self.create_html(article_title, article_content, author_name)

    # 4.写入html页面
    def create_html(self,article_title, article_content, author_name):
        html = \
        """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{}</title>
            </head>
            <body>
                <h1>{}</h1>
                {}
            </body>
            </html>
        """.format(author_name, article_title, article_content)
        self.write_html(html,article_title)

    # 5.将html内容写入html页面,并转换为pdf保存
    def write_html(self,html,article_title):
        with open('./{}.html'.format(article_title), 'w', encoding='utf-8') as f:
            f.write(html)
        try:
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_file(r'{}.html'.format(article_title), r'{}.pdf'.format(article_title), configuration=config)
            print("文件下载成功：{}".format(article_title))
        except Exception as e:
            print("文件转换失败")


    # 6.执行程序
    def main(self):
        self.request()

if __name__ == '__main__':
    url = input('请输入要下载的文章链接：')
    zhihu = Zhihu_Spider(url)
    zhihu.main()