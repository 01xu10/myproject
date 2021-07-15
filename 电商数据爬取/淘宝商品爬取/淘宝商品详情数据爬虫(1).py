from requests_html import HTMLSession
from fake_useragent import UserAgent
import os, re, json
from urllib.parse import quote
ua = UserAgent()
session = HTMLSession()


class TBTM(object):
    os_path = os.getcwd() + '/商品数据/'
    if not os.path.exists(os_path):
        os.mkdir(os_path)

    def __init__(self):
        self.title = input('请输入商品名称(例:金士顿U盘3.0):')
        self.start_url = 'https://list.tmall.com/search_product.htm?s={}&q={}'
        self.headers = {
            # 自己账号登录之后的cookie
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'upgrade-insecure-requests': '1',
            'referer': 'https://login.taobao.com/',
            'cookie': 'cna=XOLoFew4Vy0CAa8IMSySDP+Q; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; lid=%E9%A9%AC%E5%A4%B4%E5%B1%B1%E6%80%BB%E7%BB%9F; enc=S%2F5KHSTjVZZYSPUAVbGp5IUHTNauOMQMaJVqyiD8J%2FS1huMoYdZqZ9fFfyN%2BbyNH9jN55%2FHvbpm%2FeA5ysinDjg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; _uab_collina=161716788244071519261931; xlly_s=1; _m_h5_tk=df35b054970a3db60253003db90b83cd_1617263902544; _m_h5_tk_enc=0dd66b21c7a1e498bb0f34c888d56dc9; tk_trace=1; template=9cfcbdc88c0ad9d67d7511c6c911b229; tracknick=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; lgc=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; _tb_token_=eee71eee77471; cookie2=1d84d780d60efe56811d38a17fcefb04; dnk=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; _l_g_=Ug%3D%3D; unb=2565796699; cookie1=VFdmk7Z%2F8nT7ylLiBeYbj5S2L8lK5ZCXBxK7IVqMZ00%3D; login=true; cookie17=UU20sOVQOL42mQ%3D%3D; _nk_=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; sg=%E7%BB%9F9f; cq=ccp%3D0; res=scroll%3A1583*5350-client%3A1583*150-offset%3A1583*5350-screen%3A1600*900; uc1=cookie15=W5iHLLyFOGW7aA%3D%3D&cookie14=Uoe1hdNN7r7KOw%3D%3D&existShop=false&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&pas=0&cookie21=VT5L2FSpccV6%2BGPAVCK7; uc3=vt3=F8dCuAtZKmpvj50EsfA%3D&id2=UU20sOVQOL42mQ%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&nk2=odNi1ugSIEsG1Q%3D%3D; uc4=nk4=0%40o5sMsILjzh9Nu2uetVxg1eyBTdrW&id4=0%40U2%2Fz9fEqZEDrEaYBXUDcsZfn%2BNap; sgcookie=E100nnxXo%2BnAaVWjz%2BmJlREv%2Bx8RocVsFwvANKDfmUY9yKNk5h8IrLXPePk8RrO8QHvTfck7y5Iz4fePXR8FR7C2OA%3D%3D; csg=dd613770; pnm_cku822=098%23E1hvR9vUvbpvUpCkvvvvvjiWPLSU0jrnPLshQj1VPmPh1jYUP2cysj3URLdZ1jiER8OCvvBvpvpZkvhvCyEmmvpw589Cvv3vpvL3B3MmMd9Cvm3vpvvhvvCVB6CvVvhvvh27phvOvpvvpGavpC9CvvC2j6CvVP9vvhWXmvhvLhphL9mFe169Ecqvao%2FAVA9aWXxre4tYVC%2BdafmAdcvrNoqBAfpzEQyexb0lILp3ZQn%2ByXZZ%2B3%2B%2BjLoQD46XjovDN%2B3lDfUf8161iNpvvpvVph9vvvvv29hvCPMMvvvgvpvhphvvvv%3D%3D; tfstk=cfpOBdA6a20MBDjp4Ch3cmSKnu8Oaslduc_YHceAUfrnLoFuasx2ELd5Z5s4W9nd.; l=eBPkWnsqqlD2VqgbBO5Bhurza77TwIOb4rVzaNbMiInca6Qd_FZlVNCQVY3M8dtjgt1UWetzhg8L7dLHR3AgnUegJXAH9rknnxf..; isg=BIaGaCHxGvS5U_NOYIrIE3x713wI58qhuEYxx3CvcqmEcyaN2HcasWwBT-kaXcK5',
            'user-agent': ua.chrome
        }

    def parse_start_url_resp(self):
        """
        解析翻页
        :return:
        """
        """解析总页码"""
        title = quote(self.title)
        start_url = self.start_url.format(0, title)
        response = session.get(start_url, headers=self.headers)
        page_num = ''.join(re.findall('共(.*?)页', response.html.html))
        """构造翻页地址，发送请求"""
        for page in range(int(page_num)):
            next_url = self.start_url.format(page*60, title)
            self.parse_next_url_resp(next_url)
            break

    def parse_next_url_resp(self, next_url):
        """
        解析商品列表页/翻页
        :param next_url: 翻页地址
        :return:
        """
        """解析商品列表页的响应, 提取商品id"""
        response = session.get(next_url, headers=self.headers)
        shop_id_list = re.findall('data-id="(.*?)"', response.html.html)
        """商品详情页的地址拼接，然后继续请求"""
        for ship_id in shop_id_list:
            # 手机版
            shop_url_ph = 'https://detail.m.tmall.com/item.htm?id=' + ship_id
            # 电脑版
            shop_url_pc = 'https://detail.tmall.com/item.htm?id=' + ship_id
            self.parse_shop_url_resp(shop_url_ph, shop_url_pc, ship_id)
            break

    def parse_shop_url_resp(self, shop_url_ph, shop_url_pc, ship_id):
        """
        解析商品详情页
        需要双响应提取
        :param shop_url_ph: 商品详情页url地址
        :param shop_url_pc: 商品详情页url地址
        :param ship_id: 商品id
        :return:
        """
        # 手机版headers
        headers = {
            # 自己账号登录之后的cookie
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'cna=XOLoFew4Vy0CAa8IMSySDP+Q; lid=%E9%A9%AC%E5%A4%B4%E5%B1%B1%E6%80%BB%E7%BB%9F; enc=S%2F5KHSTjVZZYSPUAVbGp5IUHTNauOMQMaJVqyiD8J%2FS1huMoYdZqZ9fFfyN%2BbyNH9jN55%2FHvbpm%2FeA5ysinDjg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; template=9cfcbdc88c0ad9d67d7511c6c911b229; tracknick=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; lgc=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; _tb_token_=e57736eee645e; cookie2=1f930874abb7c95390b7fc88db747a74; xlly_s=1; dnk=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; uc1=pas=0&cookie21=Vq8l%2BKCLjhPgpfw17Hso&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie14=Uoe1hdNN4pxn5w%3D%3D; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCuAtZK3wp7%2Bm2W8g%3D&nk2=odNi1ugSIEsG1Q%3D%3D&id2=UU20sOVQOL42mQ%3D%3D; _l_g_=Ug%3D%3D; uc4=nk4=0%40o5sMsILjzh9Nu2uetVxg1eyNGJgw&id4=0%40U2%2Fz9fEqZEDrEaYBXUDcsZfrMmcG; unb=2565796699; cookie1=VFdmk7Z%2F8nT7ylLiBeYbj5S2L8lK5ZCXBxK7IVqMZ00%3D; login=true; cookie17=UU20sOVQOL42mQ%3D%3D; _nk_=%5Cu9A6C%5Cu5934%5Cu5C71%5Cu603B%5Cu7EDF; sgcookie=E100IurwLZYUJ7J8%2FpTqdrzW0M7GXBQ%2BQgw5N%2BWG8DETZHtM%2FQpJa651iQiNydmuVE2F%2FzVq%2BMjz%2F64ZyvvYDN%2Fy4A%3D%3D; sg=%E7%BB%9F9f; csg=2ca015ef; pnm_cku822=098%23E1hvh9vUvbpvj9CkvvvvvjiWPLSUljtWR2d9tj3mPmPOgjDERFSWAjlnnLMy68OCvvpvvUmmvvhvC9vhvvCvpv9CvhQhK16vCAKxfwLhdigDN%2BLvafp4VjHaD7zhQ8TJh0NEifeaHsWAcfZnIOZtIoYbD4mxfXkOjLoQD7zOdigDNr3ldE7rejvr%2B8c6lEQOKvhv8vvvvUCvpC9hvvv2UhCvmnWvvvW9phvWh9vvvACvpv11vvv2j6Cv2VeUvpvVmvvC9j3Cuvhvmvvv92sbEq8g29hvCvvvMMGgvpvhvvvvvv%3D%3D; cq=ccp%3D0; tfstk=cZWABFffTz4mrl-RYsFofPuzPz1AZdPJ7oTtBoHn9kF47EkOihWhp6OnGhuveuC..; l=eBPkWnsqqlD2V9YSBOfZourza77OQIRYouPzaNbMiOCPOA195MHAW6ZS8I8pCnGVh6U2R3yf4eUwBeYBq_fonxvOa6Fy_BHmn; _m_h5_tk=df35b054970a3db60253003db90b83cd_1617263902544; _m_h5_tk_enc=0dd66b21c7a1e498bb0f34c888d56dc9; isg=BMPDMBj2p0_aolblJUVlWEF8UodtOFd6taFUbPWgHyKZtOPWfQjnyqEmKgJfEq9y',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'
        }
        # 手机版响应
        response_ph = session.get(shop_url_ph, headers=headers)
        print(response_ph.html.html)
        # 电脑版响应
        response_pc = session.get(shop_url_pc, headers=self.headers)
        """商品的名称"""
        title = ''.join(response_pc.html.xpath('//title/text()'))
        print(title)
        """月销量/30内已售出/交易成功数量"""
        shop_go = ''.join(re.findall('"sellCount":"(.*?)"', response_ph.text))
        print(shop_go)
        """价格/淘宝价(没有设定为0)"""
        sku_price = ''.join(re.findall(r'price":\{"price":\{"priceText":"(.*?)"', response_ph.html.html))
        print(sku_price)
        """描述/服务/物流"""
        num_data = response_ph.html.xpath('//ul[@class="score"]/li/b/text()')
        print(num_data)
        """收藏宝贝(人气值)"""
        # https://count.taobao.com/counter3?_ksTS=1617196171160_264&callback=jsonp265&keys=SM_368_dsr-704392951,ICCP_1_商品的id
        url = 'https://count.taobao.com/counter3?_ksTS=1617196171160_264&callback=jsonp265&keys=SM_368_dsr-704392951,ICCP_1_' + ship_id
        resp = session.get(url).content.decode()
        result_data = ''.join(re.findall(r'jsonp262\((.*?)\);', resp))
        rq = json.loads(result_data).values()[0]
        """配送(只需要发货地)"""
        ps_data = ''.join(response_pc.html.xpath('//form[@id="J_FrmBid"]/input[7]/@value'))
        print(ps_data)
        """快递(是否免运费)"""
        kd_data = ''.join(re.findall('"快递:(.*?)"', response_ph.html.html)).replace(' ', '')
        print(kd_data)
        """承诺"""
        cn_data = ''.join(re.findall(r'items": \[(.*?)]', response_ph.html.html)) + ']'
        cn_data_list = json.loads(cn_data)
        cn_data_d = '/'.join([data['title'] for data in cn_data_list])
        print(cn_data)
        """好评/中评/差评/评论总量"""


if __name__ == '__main__':
    t = TBTM()
    t.parse_start_url_resp()
