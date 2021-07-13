# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : DY_selenium.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/7/13 22:33
# ------------------------------

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time


class DYspider(object):
    driver = webdriver.Chrome()
    """窗口最大化"""
    driver.maximize_window()
    driver.implicitly_wait(20)

    def __init__(self):
        # 登录的url
        self.login_url = 'https://passport.douyu.com/index/login'
        # 颜值分类列表页地址
        self.start_url = 'https://www.douyu.com/g_yz'

    def parse_login_url(self):
        """
        解析起始的url地址
        :return:
        """
        # 开始登录
        self.driver.get(self.login_url)
        # 给予15秒扫码时间
        time.sleep(10)
        # 访问颜值分类列表页地址
        self.driver.get(self.start_url)
        self.parse_start_url()

    def parse_start_url(self):
        """
        解析颜值分类列表页地址
        :return:
        """
        time.sleep(5)
        # 获取当前页面所有直播间的数量
        url_num = len(self.driver.find_elements_by_xpath('//*[@id="listAll"]/div[2]/ul/li/div/a'))
        for index_num in range(url_num):
            # 通过xpath定位标签，获取该标签的href链接
            url = self.driver.find_element_by_xpath(
                f'//*[@id="listAll"]/div[2]/ul/li[{index_num + 1}]/div/a').get_attribute('href')
            self.parse_hz_func(url)
        """
        1.先轰炸当前页的直播间再去翻页
        2.先翻页，获取主播直播间，最后统一轰炸
        """
        # 执行翻页
        self.parse_page_func()

    def parse_hz_func(self, url):
        """
        进入主播直播间，开始发送弹幕
        :param url:
        :return:
        """
        self.driver.implicitly_wait(10)
        # js打开新的窗口
        js = 'window.open("{}")'.format(url)
        # 执行js代码
        self.driver.execute_script(js)
        time.sleep(0.5)
        # 获取当前所有窗口
        win = self.driver.window_handles
        # 窗口切换浏览器主播页面
        self.driver.switch_to.window(win[1])
        """开始定位轰炸"""
        for i in range(10):
            self.driver.find_element_by_xpath(
                '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[3]/textarea'
            ).send_keys('主播好帅！！！')
            self.driver.find_element_by_xpath(
                '//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[3]/div[2]'
            ).click()
            time.sleep(0.5)
        self.driver.close()
        # 切换回去
        self.driver.switch_to.window(win[0])

    def parse_page_func(self):
        """
        执行翻页
        :return:
        """
        # 获取总页码
        page_num = self.driver.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/ul/li[last()-1]/a').get_attribute(
            'textContent')
        for i in range(1, int(page_num)):
            """点击翻页"""
            self.driver.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/ul/li[11]/span').click()
            self.parse_start_url()


if __name__ == '__main__':
    d = DYspider()
    d.parse_login_url()
