# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : B_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/21 17:53
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
import re
session = HTMLSession()
ua = UserAgent()


class BSpider(object):

    def __init__(self):
        self.start_url = input('请输入B站视频链接：')
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'upgrade-insecure-requests': '1',
            "cookie": "_uuid=D2282D0F-257B-845A-BDF5-C770ED288F4001440infoc; buvid3=BF17608E-FB87-4F49-A922-56FD2E284D6F18534infoc; fingerprint=5502cd4fe9637738de04bd9c3d1bdbc5; buvid_fp=BF17608E-FB87-4F49-A922-56FD2E284D6F18534infoc; SESSDATA=21607773%2C1631089673%2C71a42%2A31; bili_jct=dd92c55a6d67041ce2f3fb1650889ea8; DedeUserID=521268093; DedeUserID__ckMd5=47d541f04b605da9; sid=ivie73r8; fingerprint3=792b32adfecbe31a4aca53ab7be1ad76; fingerprint_s=bb6736758e7344a295c2ed6070cc642e; buvid_fp_plain=BF17608E-FB87-4F49-A922-56FD2E284D6F18534infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kmJYYJ)lkR0J'uYu)llkJYJ; _dfcaptcha=a46d7562a42065d43a88c053e283e876; LIVE_BUVID=AUTO8016188357987702; bsource=search_baidu; PVID=2"
        }

    def parse_start_url(self):
        """
        解析起始地址响应
        :return:
        """
        response = session.get(self.start_url, headers=self.headers).content.decode()
        # print(response)
        # 正则提取视频url地址
        mp4_url = ''.join(re.findall(r'"url":"(.*?)"', response))
        # mp4_url = mp4_url.replace(r'\u002F', '/')
        mp4_url = mp4_url.encode('latin-1').decode('unicode-escape')
        print(mp4_url)
        self.parse_save_mp4_data(mp4_url)

    def parse_save_mp4_data(self, url):
        """
        保存
        :param url: 视频的url
        :return:
        """
        data = session.get(url).content
        with open('1.mp4', 'wb')as f:
            f.write(data)
        print('保存完成')

if __name__ == '__main__':
    b = BSpider()
    b.parse_start_url()