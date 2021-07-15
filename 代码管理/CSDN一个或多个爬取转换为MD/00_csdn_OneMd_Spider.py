# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

import requests,parsel,re,os,tomd
from lxml import etree
from pprint import pprint

def main():
    # 1.url + headers
    statr_url = input("请输入你要下载的CSDN页面：")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2.对链接发起请求
    respone = requests.get(statr_url,headers=headers).text
    # pprint(respone)

    # 3.解析数据
    html_str = etree.HTML(respone)

    # 4.获取作者姓名和标题
    boke_name = html_str.xpath(r'//h1[@id="articleContentId"]/text()')[0]
    # pprint(boke_id)
    author_name = html_str.xpath(r'//a[@id="uid"]/@title')[0]
    # pprint(author_name)

    # 5.获取文章文本(html)的内容: 不能用xpath，CSS选择器！
    html_css = parsel.Selector(respone)
    article_content = html_css.css("article").get()

    # 6.将文本中的多余显示替换掉
    article_content = re.sub(r'<a.*?a>|<br>', '', article_content, re.S)
    article_content = tomd.Tomd(article_content).markdown

    # 7.创建文件夹
    os.makedirs(r"./博主：{}".format(author_name), exist_ok=True)

    # 8.保存文件到markdown
    try:
        with open('./博主：{}/{}.md'.format(author_name, boke_name), 'w' ,encoding='utf-8') as f:
            f.write('# ' + boke_name)
            f.write(article_content)
            print("***文章下载成功：{}".format(boke_name))
    except Exception as e:
        print("保存失败")



if __name__ == '__main__':
    main()