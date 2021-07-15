# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

import time, os, csv, datetime
from selenium import webdriver

class JdSpider(object):
    def __init__(self):
        self.keyword = input(r'请输入要查询的京东商品信息名称：')
        self.file_name = self.keyword + datetime.datetime.now().strftime('%Y-%m-%d')
        self.driver = webdriver.Chrome(executable_path=r'D:\selenium\chromedriver.exe')

    def request_start_url(self):
        '''
            请求初始网页
        '''
        self.driver.get(r'https://www.jd.com/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.search_goods()

    def search_goods(self):
        '''
            搜索商品数据
        '''
        self.driver.find_element_by_id('key').send_keys(self.keyword)
        self.driver.find_element_by_class_name('button').click()
        time.sleep(3)
        self.mouse_scroll()

    def mouse_scroll(self):
        '''
            鼠标滑轮滚动到底部
        '''
        for i in range(1, 13):
            js = r'scrollTo(0, {})'.format(600 * i)
            # js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %s' % (i / 20)
            self.driver.execute_script(js)
            time.sleep(1)
        self.create_dir()

    def create_dir(self):
        '''
            创建文件夹
        '''
        if not os.path.exists(r'./{}'.format('商品信息数据')):
            os.mkdir(r'./{}'.format('商品信息数据'))
        self.write_header()

    def write_header(self):
        '''
            写入csv头部信息
        '''
        if not os.path.exists(r'./{}.csv'.format(r'***商品数据保存成功：{}'.format(self.keyword))):
            csv_header = ['商品名称', '商品价格', '商品评价', '商品店铺', '商品链接']
            with open(r'./{}/{}.csv'.format('商品信息数据', self.file_name), 'w', newline='', encoding='gbk') as file_csv:
                csv_writer_header = csv.DictWriter(file_csv, csv_header)
                csv_writer_header.writeheader()
        self.get_goods_info()

    def get_goods_info(self):
        '''
            解析得到商品信息字段
        '''
        li_list = self.driver.find_elements_by_xpath('//li[@class="gl-item"]')
        for li in li_list:
            name = li.find_element_by_xpath(r'.//div[@class="p-name p-name-type-2"]/a/em').text.replace(r'京东超市','').replace(r'""', '').replace('\n', '')
            price = li.find_element_by_xpath(r'.//div[@class="p-price"]/strong/i').text + '元'
            commit = li.find_element_by_xpath(r'.//div[@class="p-commit"]/strong/a').text + '条评价'
            vendor = li.find_element_by_xpath(r'.//span[@class="J_im_icon"]/a').text
            link = li.find_element_by_xpath(r'.//div[@class="p-name p-name-type-2"]/a').get_attribute('href')
            self.save_data(name, price, commit, vendor, link)
            # print(name, price, commit, vendor, link, sep=' | ')

    def save_data(self, name, price, commit, vendor, link):
        '''
            写入csv文件主体信息
        '''
        try:
            with open(r'./{}/{}.csv'.format('商品信息数据', self.file_name), 'a+', newline='', encoding='gbk') as file_csv:
                csv_writer = csv.writer(file_csv, delimiter=',')
                csv_writer.writerow([name, price, commit, vendor, link])
                print(r'***商品数据保存成功：{}'.format(name))
        except Exception as e:
            with open(r'./{}/{}.csv'.format('商品信息数据', self.file_name), 'a+', newline='', encoding='utf-8') as file_csv:
                csv_writer = csv.writer(file_csv, delimiter=',')
                csv_writer.writerow([name, price, commit, vendor, link])
                print(r'***商品数据保存成功：{}'.format(name))

    def main(self):
        '''
            实现主要逻辑
        '''
        self.request_start_url()
        print('\n' + r'-------------文件保存成功------------------')


if __name__ == '__main__':
    jd = JdSpider()
    jd.main()