# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json
from pprint import pprint

def main():
    # 1、url + headers
    '''
        Notes: 如果url中出现特殊字符。则为一种url式加密。
        eg: 有道翻译中的：_o 和 网易云音乐中的：/#
    '''
    start_url = r'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'.replace('_o', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36'
    }

    # 2、post表单数据  使用正则 自动添加""
    while True:
        print(r'****欢迎使用贝塔男神的词典小程序****')
        word = input(r'请输入要翻译的词语：')
        form_data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": "16110565853966",
            "sign": "ac9e6a1ad007208044975e79cab12b10",
            "lts": "1611056585396",
            "bv": "7b07590bbf1761eedb1ff6dbfac3c1f0",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }

        # 3、发请求，得到响应
        response = requests.post(start_url, headers=headers, data=form_data).content.decode()
        # pprint(response)

        # 4、将json数据变成python对象（今天不用jsonpath）
        json_str = json.loads(response)
        # pprint(json_str)

        # 5、使用字典基础班知识提取数据
        result = json_str["translateResult"][0][0]["tgt"]
        print(r'翻译的结果是：{}'.format(result))

if __name__ == '__main__':
    main()