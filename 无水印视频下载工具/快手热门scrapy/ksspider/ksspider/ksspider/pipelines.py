# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os


class KsspiderPipeline(object):
    def __init__(self):
        self.os_path = os.getcwd() + '/快手视频/'
        if not os.path.exists(self.os_path):
            os.mkdir(self.os_path)

    def process_item(self, item, spider):
        dict_data = dict(item)
        with open(self.os_path + dict_data['title'] + '.mp4', 'wb')as f:
            f.write(dict_data['data'])
        print(f"{dict_data['title']}-----------------下载完成--------------logging！！！")
        return item
