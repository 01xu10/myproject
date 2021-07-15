# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : adoutu_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/3/26 13:19
# ------------------------------
import requests,random,os,re
from lxml import etree
from pprint import pprint

class adoutu_spider(object):
    # url + headers
    def __init__(self):
        self.start_url = r'http://adoutu.com/article/list/{}'
        self.USER_AGENT = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                           'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                           'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                           'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2']

        self.headers={
            'User-Agent':random.choice(self.USER_AGENT)
        }

    # 2.请求start_url
    def first_resquest(self):
        for i in range(1,20):
            response = requests.get(self.start_url.format(i),headers=self.headers).text
            # pprint(response)
            html_str = etree.HTML(response)
            url_list = html_str.xpath('//div[@class="list-group article-part"]/div/a/@href')
            # pprint(url_list)
            img_titles = html_str.xpath('//div[@class="list-group article-part"]/div/a/@title')
            # pprint(self.img_titles)
            for url,img_title in zip(url_list,img_titles):
                url = 'http://adoutu.com' + url
                self.img_title = img_title
                self.second_resquest(url)

    # 3.请求每个类型表情包的url,获取后缀，名称
    def second_resquest(self,url):
        response = requests.get(url,headers=self.headers).text
        # pprint(response)
        img_urls = re.findall('<img src="(.*?)" alt',response)[1:]
        img_names = re.findall('alt="(.*?) " title="',response)
        # pprint(img_names)
        i = 1
        for img_url,img_name in zip(img_urls,img_names):
            postfix = img_url.split('.')[-1]
            if len(postfix)>4:
                postfix = 'jpg'
                img_name = '图{}'.format(i)
                i += 1
            # print(postfix,img_name)
            self.save_img_info(img_url,postfix,img_name)

    # 4.保存图片
    def save_img_info(self,img_url,postfix,img_name):
        # 创建文件夹
        os.makedirs('./表情包/{}'.format(self.img_title), exist_ok=True)
        # 保存图片数据
        img_content = requests.get(img_url,headers=self.headers).content
        try:
            with open('./表情包/{}/{}.{}'.format(self.img_title,img_name,postfix),'wb') as f:
                f.write(img_content)
                print('表情包：{}.{}，保存成功！'.format(img_name,postfix))
        except Exception as e:
            print('{}表情包下载失败'.format())

    # 5.执行函数
    def main(self):
        self.first_resquest()

if __name__ == '__main__':
    abaotu = adoutu_spider()
    abaotu.main()