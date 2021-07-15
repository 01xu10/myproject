# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, jsonpath, os
from pprint import pprint

def main():
    start_url = r'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2、第一次请求，获取hero_id
    response = requests.get(start_url, headers=headers).json()
    pprint(response)
    hero_ids = jsonpath.jsonpath(response, '$..heroId')
    # pprint(hero_ids)p
    hero_names = jsonpath.jsonpath(response, '$..name')
    # pprint(hero_name)

    # 3、构造hero_info页面   hero_info里面是没有炫彩皮肤的
    for hero_id, hero_name in zip(hero_ids, hero_names):
        hero_info_url = r'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(hero_id)

        # 4、请求得到hero_img_info
        hero_img_info = requests.get(hero_info_url, headers=headers).json()
        # pprint(hero_img_info)

        # 5、解析得到hero_skin_names, hero_skin_urls
        hero_skin_names = jsonpath.jsonpath(hero_img_info, '$..name')[2::]
        # pprint(hero_skin_names)
        hero_skin_urls = jsonpath.jsonpath(hero_img_info, '$..mainImg')[1::]
        # pprint(hero_skin_urls)

        # 6、遍历循环得到hero_skin_name, hero_skin_url
        for hero_skin_name, hero_skin_url in zip(hero_skin_names, hero_skin_urls):
            # pprint(hero_skin_url)

            # 7、对图片发请请求，得到二进制数据 img_content
            try:
                img_content = requests.get(hero_skin_url, headers=headers).content
                # pprint(img_content)
            except Exception as e:
                continue

            # 8、创建文件夹
            os.makedirs(r'./{}'.format(hero_name), exist_ok=True)

            # 9、保存数据
            try:
                with open(r'./{}/{}.jpg'.format(hero_name, hero_skin_name), 'wb') as f:
                    f.write(img_content)
                    print('**图片正在下载：{}/{}.jpg'.format(hero_name, hero_skin_name))
            except Exception as e:
                continue

if __name__ == '__main__':
    main()


