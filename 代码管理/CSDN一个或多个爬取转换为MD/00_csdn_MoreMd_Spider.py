# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------


import requests,re, os, tomd, parsel
from lxml import etree
from pprint import pprint


def main():
    # 1、url + headers
    # # start_url = input('请输入CSDN博客主页链接：')
    start_url = 'https://blog.csdn.net/Six23333'
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36',
        'Referer': 'https://blog.csdn.net/weixin_48057068'
    }

    # 2、请求获取响应数据
    response = requests.get(start_url, headers=headers).text
    # print(response)

    # 3、解析获取 boke_ids, author_name, author_id
    html_str_first = etree.HTML(response)
    boke_ids = html_str_first.xpath(r'//div[@class="article-item-box csdn-tracking-statistics"]/@data-articleid')
    # pprint(boke_ids)
    author_name = html_str_first.xpath(r'//a[@id="uid"]/@title')[0]
    # print(author_name)
    author_id = re.findall(r'https://blog.csdn.net/(.*?\d$)', start_url)[0]
    # pprint(author_id)


    # 4、遍历获取boke_id, 构造boke_url
    for boke_id in boke_ids:
        boke_url = r'https://blog.csdn.net/{}/article/details/{}'.format(author_id, boke_id)
        # pprint(boke_url)

        # 5、发请求，获取响应数据
        response = requests.get(boke_url, headers=headers).text
        # pprint(response)

        # 6、解析得到文件名， 作者名
        html_str_first = etree.HTML(response)
        article_name = html_str_first.xpath(r'head/title/text()')[0]
        # article_name = html_str_first.xpath(r'h1[@class="title-article"]/text()')[0]
        print(article_name)

        # 7、解析得到文本主体内容， 删除相应不用的格式
        html_str_second = parsel.Selector(response)
        content = html_str_second.css('article').get()

        content = re.sub(r'<a.*?a>|<br>', '', content, re.S)
        content = tomd.Tomd(content).markdown

        # 8、创建文件夹
        os.makedirs(r'./{}'.format(author_name),exist_ok=True)


        # 9、保存文件到markdown
        try:
            with open(r'{}/{}.md'.format(author_name, article_name), 'w', encoding='utf-8') as f:
                f.write('# ' + article_name)
                f.write(content)
                print(r'***成功下载：{}'.format(article_name))
        except Exception as e:
            continue


if __name__ == '__main__':
    main()