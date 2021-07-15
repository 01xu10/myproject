# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        with open('douban.txt', 'w')as f:
            f.write(str(dict(item)))
        print('数据保存完成==============logging！！！')
        return item
