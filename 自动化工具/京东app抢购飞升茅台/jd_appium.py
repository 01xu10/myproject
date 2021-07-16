# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : jd_appium.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/7/16 9:21
# ------------------------------
# 导入webdriver
from appium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import time

"""定时启动"""
sched = BlockingScheduler()
def qg():
    # 初始化参数
    desired_caps = {
        'platformName': 'Android',  # 被测手机是安卓
        'platformVersion': '10',  # 手机安卓版本
        'deviceName': 'MI8',  # 设备名，安卓手机可以随意填写
        'appPackage': 'com.jingdong.app.mall',  # 启动APP Package名称
        'appActivity': '.main.MainActivity ',  # 启动Activity名称
        'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
        'resetKeyboard': True,  # 执行完程序恢复原来输入法
        'noReset': True,  # 不要重置App，如果为False的话，执行完脚本后，app的数据会清空，比如你原本登录了，执行完脚本后就退出登录了
        'newCommandTimeout': 6000,
    }
    # 连接Appium Server，初始化自动化环境
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    # 点击搜索框
    time.sleep(5)
    driver.find_element_by_class_name('android.widget.ViewFlipper').click()
    # 输入搜索内容
    time.sleep(1)
    driver.find_element_by_id('com.jd.lib.search.feature:id/a3g').send_keys('飞天茅台')
    # 点击搜索
    driver.find_element_by_xpath('//android.widget.TextView[@content-desc="搜索，按钮"]').click()
    # 点击商品
    time.sleep(1)
    driver.find_element_by_xpath('//android.widget.TextView[@content-desc="茅台 飞天酱香型白酒 500ml "]').click()
    # 点击抢购
    time.sleep(1)
    """定时抢购"""
    sched = BlockingScheduler()
    def dj():
        num = 0
        try:
            while True:
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                driver.find_element_by_id('com.jd.lib.productdetail.feature:id/add_2_car').click()
                print(r'抢购点击{}次'.format(num))
                num += 10
        except:
            print('抢购成功')

    # 表示2017年3月22日17时19分07秒执行该程序
    """定时抢购设置"""
    sched.add_job(dj, 'cron', year=2021, month=6, day=29, hour=11, minute=59, second=59)
    sched.start()
"""定时启动设置"""
# 表示2017年3月22日17时19分07秒执行该程序
sched.add_job(qg, 'cron', year=2021, month=6, day=29, hour=11, minute=59, second=00)
sched.start()

