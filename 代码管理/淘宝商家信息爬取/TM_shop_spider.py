# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : TM_shop_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/16 13:59
# ------------------------------

from requests_html import HTMLSession
from fake_useragent import UserAgent
from lxml import etree
import re, time

session = HTMLSession()
ua = UserAgent()
'''
    s ：页码       user_id ：店铺id
    https://list.tmall.com/search_shopitem.htm?s=0&user_id=2786278078
    https://list.tmall.com/search_shopitem.htm?s=60&user_id=2786278078
    
'''


class TM_shop_spider(object):
    def __init__(self):
        self.start_url = 'https://list.tmall.com/search_shopitem.htm?s={}&user_id=2206773587214'
        self.headers = {
            'cookie': 'cna=esBjGPb+5ysCAXjmfgYrwjLT; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E4%BC%BC%E6%B0%B4%E6%B5%81%E5%B9%B4%E6%8D%A2%E6%9D%A5%E4%B8%80%E7%89%87%E6%80%9D%E5%BF%B5ii; enc=kDq%2FKkNRBYPT6WFwzCS45lXiFr8IsWfuC3nAJ%2FEGk5YCBpkIiQD4LsXs4%2B2peY7l9%2BgG7uCxJFMx0CZrtneoCw%3D%3D; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; _uab_collina=161849707401292616928831; sm4=440100; xlly_s=1; _m_h5_tk=7ee2a48563096ca331fa9d72932756d4_1618595441894; _m_h5_tk_enc=87089433c3452460dfecd7e7b6233eef; t=f1ac3f66d2d49321bf49a74fe96ef4d5; tracknick=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; lgc=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; _tb_token_=ee33071ebf338; cookie2=1780d5181c022415536a55c91437347a; x5sec=7b22746d616c6c7365617263683b32223a22336365666534633435336162356166623533316263366461323538373239323943496e3736594d47454a432f7066616c362b656a57526f4d4d6a6b354f5445304d6a4d354d7a73784d4b4c5468594c382f2f2f2f2f77453d227d; dnk=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; uc1=existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&pas=0&cookie14=Uoe1iua9pWzq4g%3D%3D&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=qG4xH1%2BrhA9Q1R3bBUhyrTOKMxbBow%3D%3D&vt3=F8dCuwpkhc4BfqJG7zY%3D&id2=UUGrf6z4e6WENQ%3D%3D; _l_g_=Ug%3D%3D; uc4=id4=0%40U2OcT2LaNdpEAsP2rjbmiAKAxc1X&nk4=0%40qlXnga8AYEMW1VrMSD5nndqSKiKIw4X3y0VewexsPTEE; unb=2999142393; cookie1=BxeAZ7VBFfmr3eyRQFuwIvIGjU8PcS1BkB6A8Q7UpOk%3D; login=true; cookie17=UUGrf6z4e6WENQ%3D%3D; _nk_=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; sgcookie=E100COh3WXk%2FZOFgLV1fc3SZ11BsEKBfzH22IDePKeV%2Ben%2FAAyvcS%2B3wLVGzhmaXCOZN49VfWh8iiRwUBYtqP1EaWw%3D%3D; sg=i32; csg=ddbeb06e; pnm_cku822=098%23E1hv89vUvbpvUpCkvvvvvjiWPLLO6jrURsSOgjljPmPhgjrnPssWtjDPPLSpgjr8R4OCvvpvvUmmRvhvCvvvvvvRvpvhMMGvvvvCvvOvCvvvphvUvpCWCElMvvwQTWex6fItb9TxfJBl5dUf8rBl%2BE7rejyyYExrt8g7EcqyaNoxdX3tEbmxfwmK5kx%2FQj7%2BD40wjLVDYWLp5E3%2BVd0DyOvO5f9Cvm9vvvvpphvvQpvv93lvpv3Lvvv2vhCv2UhvvvWvphvWmpvv9kBvpvQ1kvhvC99vvOCgp49Cvv9vvUvG5KEwcp%3D%3D; res=scroll%3A1322*5266-client%3A1322*724-offset%3A1322*5266-screen%3A1536*864; cq=ccp%3D0; tfstk=cvlGBQVetAy_UQynFCNs59dAmUKRZXJafjlETjfSQmr_-lcFiABFUd_9-lniMt1..; l=eBgBRF5VjJ1jHzpSBOfaourza779sIRvSuPzaNbMiOCPO0165LC1W6aZZrTBCnGVhsnJJ3yIzizJBeYBqSX6rVms0xVS3xkmn; isg=BBoat9kYLm89w6LcAjtiS8xoa8A8S54lMKSDqiSTx614l7rRDd8wNSllZ2MLcha9',
            'referer': 'https://login.taobao.com/',
            'upgrade-insecure-requests': '1',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'user-agent': ua.chrome
        }

        self.headers_ph = {
            'cookie': 'cna=esBjGPb+5ysCAXjmfgYrwjLT; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E4%BC%BC%E6%B0%B4%E6%B5%81%E5%B9%B4%E6%8D%A2%E6%9D%A5%E4%B8%80%E7%89%87%E6%80%9D%E5%BF%B5ii; enc=kDq%2FKkNRBYPT6WFwzCS45lXiFr8IsWfuC3nAJ%2FEGk5YCBpkIiQD4LsXs4%2B2peY7l9%2BgG7uCxJFMx0CZrtneoCw%3D%3D; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; _uab_collina=161849707401292616928831; sm4=440100; dnk=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; tracknick=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; lgc=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; login=true; cookie2=1117f47b3aafe35d0e4a5a4eda1baa5b; t=39ed7c7b49084a7d96127f0a38cb7537; _tb_token_=53435e7b51391; xlly_s=1; _m_h5_tk=7ee2a48563096ca331fa9d72932756d4_1618595441894; _m_h5_tk_enc=87089433c3452460dfecd7e7b6233eef; uc1=cookie14=Uoe1iuWbzpQyiw%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreK%2BBd&pas=0&cookie15=V32FPkk%2Fw0dUvg%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D; uc3=nk2=qG4xH1%2BrhA9Q1R3bBUhyrTOKMxbBow%3D%3D&id2=UUGrf6z4e6WENQ%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCuwpnnJx98TO%2B3G8%3D; _l_g_=Ug%3D%3D; uc4=nk4=0%40qlXnga8AYEMW1VrMSD5nndqSKiKIw4X3y0Vewh9x8KiZ&id4=0%40U2OcT2LaNdpEAsP2rjbmi0ZxKzqA; unb=2999142393; cookie1=BxeAZ7VBFfmr3eyRQFuwIvIGjU8PcS1BkB6A8Q7UpOk%3D; cookie17=UUGrf6z4e6WENQ%3D%3D; _nk_=%5Cu4F3C%5Cu6C34%5Cu6D41%5Cu5E74%5Cu6362%5Cu6765%5Cu4E00%5Cu7247%5Cu601D%5Cu5FF5ii; sgcookie=E100Ts9UeM%2Bk7U78wSmSOGNOH7EHxNk1pOTz8hPlj4aMm9WTnIfuTLah5z2k8wY5G26bLNfYnfG4KWSeSKkOWP7DMQ%3D%3D; sg=i32; csg=5ac3b4fc; cq=ccp%3D0; x5sec=7b22746d616c6c7365617263683b32223a2230333166633966646539366538656536626639353536373765356534333931374350372f356f4d47454f32507a7547763075574c42686f4d4d6a6b354f5445304d6a4d354d7a73784d4f5057684b62352f2f2f2f2f77453d227d; res=scroll%3A1519*5266-client%3A1519*731-offset%3A1519*5266-screen%3A1536*864; pnm_cku822=098%23E1hvhvvUvbpvUvCkvvvvvjiWPLLZtjinRFFwzjnEPmPWljYWn2svljrmPF5ZQjlbRvhvCvvvvvvvvpvVvvpvvhCvmvhvLCpUNQvjPwex6aZtn0vHfwBlYb8rwoA%2BkE7tR3H%2BvSLhlbvqrADn9W2%2BFfmtEpcpTWexRdIAcUmtYE7reC6k1nsI1EI7nDeDyO2vSdTUvpvVmvvC9j3Cuvhvmvvv92Af2Z7%2BKvhv8vvvvvCvpvvvvvv2vhCvmVGvvvWvphvW9pvvvQCvpvQEvvv2vhCv2vyRvpvhvv2MMTOCvvpvvUmm; tfstk=cv0RBQqSVKvl3dNx_0KcOdxtv30RZG18K_wdJQKM34iJN5QdiwuiWcZMVWW8kIC..; l=eBgBRF5VjJ1jHanyBOfaourza779TIRvSuPzaNbMiOCP_yCe59aCW6a15O8wCnGVhsBBJ3yIzizJBeYBqHxnnxvt0xVS3xkmn; isg=BAMDc77hZxMBJCv7cyjbxK1LkseteJe68WdKjTXgDmLZ9CMWvEwTC6NuboS64e-y',
            'referer': 'https://list.tmall.com/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not\"A\\Brand";v="99"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/89.0.4389.128 Mobile Safari/537.36'
        }

    def parse_start_url(self):
        print('========正在进入店铺=========')
        time.sleep(2)
        page = 1
        i = 0
        while i < page:
            response = session.get(self.start_url.format(i * 60), headers=self.headers)
            # print(response.text)
            page = int(''.join(re.findall('共(.*?)页', response.text)))
            # print(page)
            commodity_id_list = response.html.xpath('//p[@class="productStatus"]/span[@data-icon="small"]/@data-item')
            for commodity_id in commodity_id_list:
                commodity_pc_url = 'https://detail.tmall.com/item.htm?id=' + commodity_id
                commodity_ph_url = 'https://detail.m.tmall.com/item.htm?id=' + commodity_id
                self.parse_commodity_url(commodity_pc_url, commodity_ph_url, commodity_id)
            i += 1
        print('***********商品下载完毕************')

    def parse_commodity_url(self, commodity_pc_url, commodity_ph_url, commodity_id):
        '''
        解析商品页的数据
        :param commodity_pc_url:  pc端url
        :param commodity_ph_url:  phone端url
        :param commodity_id: 商品id
        :return:
        '''
        time.sleep(1)
        response_pc = session.get(commodity_pc_url, headers=self.headers).text.replace('    ', '')
        time.sleep(1)
        response_ph = session.get(commodity_ph_url, headers=self.headers_ph)

        '''需求1：产品参数 phone端'''
        # pprint(response_ph.text)
        good = re.findall('"groupProps":\[.*?}\]}]', response_ph.text)[0]
        # print(good, type(good))
        name = ''.join(re.findall('"品牌":"(.*?) "', good))
        single = ''.join(re.findall('单品":"(.*?) "', good))
        effect = ''.join(re.findall('"功效":"(.*?) "', good))
        data = ''.join(re.findall('日期范围":"(.*?) "', good))
        skin = ''.join(re.findall('"适合肤质":"(.*?) "', good))
        com_name = name + single

        '''需求2：服务承诺 pc端'''
        html_str = etree.HTML(response_pc)
        service_promise_1 = '-'.join(html_str.xpath('//ul[@class="tb-serPromise"]/li/a/text()'))
        service_promise = service_promise_1.replace('\r\n', '')
        # print(service_promise)

        '''需求3：价格'''
        price = re.findall('"price":(.*?)"newExtraPrices"', response_ph.text)[0]
        price_before = ''.join(re.findall('"priceText":"(.*?)",', price))
        # print(price_before)
        price_1 = ''.join(re.findall('"priceTag":(.*?)"priceAttractData"', response_ph.text))
        # print(price_1)
        price_now = ''.join(re.findall('"priceText":"(.*?)"', price_1))
        # print(price_now)

        '''需求4：评价总数'''
        comment_num = ''.join(re.findall('"rate":(.*?)"rateList"', response_ph.text))
        totalCount = ''.join(re.findall('"totalCount":(.*?),"', comment_num))
        if totalCount == '':
            com_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId={}'.format(commodity_id)
            resp = session.get(com_url, headers=self.headers).text
            totalCount = ''.join(re.findall('"rateTotal":(.*?)}', resp))
        # print(totalCount)

        '''需求5：收藏商品人气'''
        hot_url = 'https://count.taobao.com/counter3?_ksTS=1618587177342_224&callback=jsonp225&keys=SM_368_dsr-2786278078,ICCP_1_{}'.format(
            commodity_id)
        response = session.get(hot_url, headers=self.headers)
        # print(response.text)
        hot_num = re.findall(f'ICCP_1_{commodity_id}":(.*?),"', response.text)[0]
        print(com_name, name, single, effect, data, skin, price_before, price_now, totalCount, hot_num, service_promise)
        print('================')
        print('')


if __name__ == '__main__':
    shop = TM_shop_spider()
    shop.parse_start_url()
