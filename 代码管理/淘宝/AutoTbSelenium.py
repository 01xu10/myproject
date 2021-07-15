# !/usr/bin/env python
# -*- coding: utf-8 -*-
''''''

'''
    淘宝秒杀：正常的步骤！
        1、打开浏览器
        2、https://www.taobao.com/
        3、登录淘宝
        4、点击购物车
        5、选择商品  简单一点： 点击全选
        6、点击  结算
        7、点击提交订单
        
    写selenium的时候，建议 不要使用 函数式编程！
    直接方式  或者 面向对象！  
    如果使用函数式编程： 他会自动关闭浏览器！导致我们不爽！
    
    欠缺部分：
        你老婆采购的时间：00:00分抢一个东西！时间判断！   基础班知识！
            提示： 当前的时间>= 定时的时间  是不是抢购
            
        建议 用面向对象去实现一次
'''

import time
from selenium import webdriver


# 1、打开浏览器： 创建一个浏览器对象(实例化)！  pip install selenium  Chrome:谷歌浏览器
driver = webdriver.Chrome(executable_path=r'D:\selenium\chromedriver.exe')

# 2、窗口最大化  max
time.sleep(1)
driver.maximize_window()

# 3、访问： https://www.taobao.com/  get()方法
driver.get('https://www.taobao.com/')
time.sleep(4)

# 4、登录淘宝-A  -- 找到 请登录  这个标签   点击： click
driver.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()

# 5、登录淘宝-B  扫码登录
time.sleep(2)
driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()

# 6、从你裤裆  掏出手机  要时间！
time.sleep(15)

# 7、登录成功了？ 点击购物车！
driver.find_element_by_xpath('//*[@id="J_MiniCart"]').click()

# 8、点击全选 选择商品
time.sleep(2)
driver.find_element_by_xpath('//*[@id="J_SelectAll1"]/div/label').click()

# 9、点击结算
time.sleep(2)
driver.find_element_by_xpath('//*[@id="J_Go"]').click()

# 10、点击提交订单
time.sleep(4)
driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div/a[2]').click()














