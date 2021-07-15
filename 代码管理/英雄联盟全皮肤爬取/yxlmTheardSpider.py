# !/usr/bin/env python
# -*- coding: utf-8 -*-


import requests, jsonpath, threading, os


class Lol(object):
    def __init__(self):
        # 初始化hero_list hero_info_url, headers
        self.hero_list_url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
        self.hero_info_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36'
        }

    def parse_first(self):
        # 得到 hero_ids, hero_names
        response = requests.get(self.hero_list_url, headers=self.headers).json()
        hero_ids = jsonpath.jsonpath(response, '$..heroId')
        hero_names = jsonpath.jsonpath(response, '$..name')
        for hero_name, hero_id in zip(hero_names, hero_ids):
            self.parse_second(hero_name, hero_id)

    def parse_second(self, hero_name, hero_id):
        # 得到phone_img_urls， computer_img_urls， skin_names
        hero_info = requests.get(self.hero_info_url.format(hero_id), headers=self.headers).json()
        phone_img_urls = jsonpath.jsonpath(hero_info, '$..loadingImg')[1::]
        computer_img_urls = jsonpath.jsonpath(hero_info, '$..mainImg')[1::]
        skin_names = jsonpath.jsonpath(hero_info, '$..name')[2::]
        for phone_img_url, computer_img_url, skin_name in zip(phone_img_urls, computer_img_urls,skin_names):
            self.get_content(phone_img_url, computer_img_url, skin_name, hero_name)

    def get_content(self, phone_img_url, computer_img_url, skin_name, hero_name):
        # 得到phone_img_content，computer_img_content
        try:
            phone_img_content = requests.get(phone_img_url, headers=self.headers).content
            computer_img_content = requests.get(computer_img_url, headers=self.headers).content
        except Exception as e:
            print('炫彩皮肤不存在')
        self.thearding_sava(phone_img_content, computer_img_content, skin_name, hero_name)

    def save_phone_img(self, phone_img_content, skin_name, hero_name):
        # 保存手机版的壁纸
        os.makedirs('{}/{}'.format('手机版壁纸', hero_name), exist_ok=True)
        with open('{}/{}/{}.jpg'.format('手机版壁纸', hero_name, skin_name), 'wb') as f:
            f.write(phone_img_content)
            print('正在手机版壁纸：{}/{}.jpg'.format(hero_name, skin_name))

    def save_computer_img(self, computer_img_content, skin_name, hero_name):
        # 保存电脑版的壁纸
        os.makedirs('{}/{}'.format('电脑版壁纸', hero_name), exist_ok=True)
        with open('{}/{}/{}.jpg'.format('电脑版壁纸', hero_name, skin_name), 'wb') as f:
            f.write(computer_img_content)
            print('正在电脑版壁纸：{}/{}.jpg'.format(hero_name, skin_name))

    def thearding_save(self, phone_img_content, computer_img_content, skin_name, hero_name):
        threading.Thread(target=self.save_phone_img, args=(phone_img_content, skin_name, hero_name)).start()
        threading.Thread(target=self.save_computer_img, args=(computer_img_content, skin_name, hero_name)).start()

    def main(self):
        self.parse_first()

if __name__ == '__main__':
    lol = Lol()
    lol.main()