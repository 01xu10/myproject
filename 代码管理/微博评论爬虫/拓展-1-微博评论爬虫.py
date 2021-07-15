"""
需求：
    爬取微博大明星任意微博动态的评论

数据需求：
    微博评论区用户评论内容，评论时间，点赞数，用户名，用户id，用户性别，用户地区，用户微博数，用户粉丝数，用户关注数，二级评论
"""

# 思路：
# 手机模式进入微博动态详情页 --> 获取评论区地址 --> 下一页的max_id在当前(上一页)评论页

"""
难点: 
    高并发的处理
    headers请求头的设计
    递归回调逻辑的处理
    cookie的介绍
反爬：
    IP，与cookie受限
    解决方案：多cookie与IP代理的使用
"""

# 用户登录之后的cookie，在退出浏览器之后，这个cookie还有效吗？
# from requests_html import HTMLSession
# from fake_useragent import UserAgent
# ua = UserAgent()
# session = HTMLSession()
#
# headers = {
#     'Cookie': 'douban-fav-remind=1; _vwo_uuid_v2=D4EDEB274998EF9670C11D9789C7C93BA|78d9187b2c765cfc0c80ed7767048abb; _ga=GA1.2.1416200646.1568801148; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1596096825; __utmv=30149280.22281; ll="118267"; bid=qRD3Npr76rc; douban-profile-remind=1; __yadk_uid=3y414E8QNxM7v369WbTHNe5N5cM03gHZ; push_noty_num=0; push_doumail_num=0; __gads=ID=aa84b9a3cc19bd7e-22ea25ca5ec60093:T=1615552760:RT=1615552760:S=ALNI_MY2lOLuM9i5_UxzjfnZMlydsO-WiA; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1619611243%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DZv-exJOLpI45RNiNzPKvG2LbeusgWQc0TyX_9PLBUQNSrRObinPZZWm8oAwlxEDR%26wd%3D%26eqid%3De65703f7000e108d0000000660894e66%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1416200646.1568801148.1619007442.1619611244.63; __utmc=30149280; __utmz=30149280.1619611244.63.49.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="222817495:s7Gn7yz9VAk"; ck=gXJF; _pk_id.100001.8cb4=9d88f7423196bb38.1570610339.47.1619611256.1617711451.; __utmb=30149280.3.10.1619611244',
#     'Host': 'www.douban.com',
#     'Referer': 'https://www.douban.com/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
# }
#
# start_url = 'https://www.douban.com/'
#
# response = session.get(start_url, headers=headers).content.decode()
# print(response)
# """
# cookie的两种机制：
#     1.这一个cookie有过期时间，不受浏览器的退出影响
#
#     2.浏览器退出，cookie失效
# """


# https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id_type=0
# https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id=1064227722843728&max_id_type=0

# from requests_html import HTMLSession
# from fake_useragent import UserAgent
# import jsonpath
# ua = UserAgent()
# session = HTMLSession()
#
# url = 'https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id_type=0'
#
#
# headers = {
#     'cookie': 'WEIBOCN_FROM=1110005030; SUB=_2A25NjSBtDeRhGeFL61AR8SrEzTyIHXVujkAlrDV6PUJbkdB-LWvykW1NQrcPFFbqhskrtto-td6FjWxVJsVgJJtj; _T_WM=87244903697; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4631028247299825%26luicode%3D20000061%26lfid%3D4631028247299825%26uicode%3D20000061%26fid%3D4631028247299825; XSRF-TOKEN=51a6f7',
#     'mweibo-pwa': '1',
#     'referer': 'https://m.weibo.cn/status/Kd1byuD17?type=comment&jumpfrom=weibocom',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
#     'x-xsrf-token': '51a6f7'
# }
#
# response = session.get(url, headers=headers).json()
# max_id = response['data']['max_id']
# # print(max_id)
# next_url = f'https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id={max_id}&max_id_type=0'
# resp = session.get(next_url, headers=headers).json()
# # print(resp)
#
# max_id = resp['data']['max_id']
# print(max_id)
# next_url_1 = f'https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id={max_id}&max_id_type=0'
# resp = session.get(next_url_1, headers=headers).json()
# print(resp)

"""
二级评论解析                                   4631028247299825
                                             4631028344294714
https://m.weibo.cn/comments/hotFlowChild?cid=4631028344294714&max_id=0&max_id_type=0
https://m.weibo.cn/comments/hotFlowChild?cid=4631028439714734&max_id=0&max_id_type=0
"""


from requests_html import HTMLSession
from fake_useragent import UserAgent
import os, xlwt, xlrd, time, random
from xlutils.copy import copy
from datetime import datetime
ua = UserAgent()
session = HTMLSession()


class WBSpider(object):

    def __init__(self):
        self.start_url = 'https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id_type=0'
        self.headers = {
            'cookie': 'WEIBOCN_FROM=1110005030; SUB=_2A25NjSBtDeRhGeFL61AR8SrEzTyIHXVujkAlrDV6PUJbkdB-LWvykW1NQrcPFFbqhskrtto-td6FjWxVJsVgJJtj; _T_WM=87244903697; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4631028247299825%26luicode%3D20000061%26lfid%3D4631028247299825%26uicode%3D20000061%26fid%3D4631028247299825; XSRF-TOKEN=9b97fb',
            'mweibo-pwa': '1',
            'referer': 'https://m.weibo.cn/status/Kd1byuD17?type=comment&jumpfrom=weibocom',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?1',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': '9b97fb'
        }

    def parse_start_url(self):
        """
        解析评论第一页的响应
        :return:
        """
        response_json = session.get(self.start_url, headers=self.headers).json()
        """提取翻页的id"""
        max_id = response_json['data']['max_id']
        """将第一页的响应，传递到解析响应的方法中"""
        self.parse_content_info(response_json)
        """传递到翻页函数，构造翻页请求"""
        self.parse_page_max_id(max_id)

    def parse_page_max_id(self, max_id):
        """
        翻页处理的函数
        :param max_id:
        :return:
        """
        next_url = f'https://m.weibo.cn/comments/hotflow?id=4631028247299825&mid=4631028247299825&max_id={max_id}&max_id_type=0'
        response = session.get(next_url, headers=self.headers).json()
        """提取翻页的id"""
        max_id = response['data']['max_id']
        """解析响应的评论"""
        self.parse_content_info(response)
        """回调处理：递归"""
        self.parse_page_max_id(max_id)

    def parse_content_info(self, response_data_json):
        """
        翻页地址的响应解析
        :param response_data_json: 翻页地址的响应
        :return:
        """
        data_json_list = response_data_json['data']['data']
        for data_json in data_json_list:
            # 评论时间   格林威治时间
            start_time = data_json['created_at']
            time_t = '%a %b %d %H:%M:%S %z %Y'
            start_time = str(datetime.strptime(start_time, time_t))
            # 评论点赞量
            like_count = data_json['like_count']
            # 评论内容
            text = data_json['text']
            # 用户的昵称
            screen_name = data_json['user']['screen_name']
            # 用户的性别
            gender = data_json['user']['gender']
            gender = '女' if gender == 'f' else '男'
            # 用户的id
            user_id = data_json['user']['id']
            # 用户主页地址--访问即可获取粉丝量 & 关注量
            user_info_url = data_json['user']['profile_url']
            # 微博认证
            verified_reason = data_json['user']['verified_reason']
            """二级评论id"""
            content_id = data_json['mid']
            list_big_data = [start_time, like_count, text, screen_name, gender, user_id, user_info_url, verified_reason]
            data = {
                '一级评论数据': list_big_data
            }
            """保存数据"""
            self.save_data_to_execl(data)
            print('一级评论解析成功====logging！！！')
            """调用解析二级评论方法"""
            self.parse_two_page_info_response(content_id)

    def parse_two_page_info_response(self, content_id):
        """
        解析二级评论
        :param content_id: 二级评论id
        :return:
        """
        """二级评论的url地址"""
        two_content_url = f'https://m.weibo.cn/comments/hotFlowChild?cid={content_id}&max_id=0&max_id_type=0'
        headers = {
            'cookie': 'WEIBOCN_FROM=1110005030; SUB=_2A25NjSBtDeRhGeFL61AR8SrEzTyIHXVujkAlrDV6PUJbkdB-LWvykW1NQrcPFFbqhskrtto-td6FjWxVJsVgJJtj; _T_WM=87244903697; MLOGIN=1; XSRF-TOKEN=dd6fa0; M_WEIBOCN_PARAMS=luicode%3D20000061%26lfid%3D4631028247299825%26oid%3D4631028247299825%26fid%3D1076035893081964%26uicode%3D10000011',
            'mweibo-pwa': '1',
            'referer': f'https://m.weibo.cn/detail/Kd1byuD17?cid={content_id}',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?1',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': 'dd6fa0'
        }
        response = session.get(two_content_url, headers=headers).json()
        """解析评论内容"""
        self.parse_two_info_response_content(response, content_id)
        """提取翻页的id"""
        max_id = response['max_id']
        self.parse_two_page_response(max_id, content_id, headers)

    def parse_two_page_response(self, max_id, content_id, headers):
        """
        解析二级评论的翻页
        :param max_id: 二级评论翻页的max_id
        :param content_id: 二级评论的max_id
        :param headers: 二级评论请求头
        :return:
        """
        next_url = f'https://m.weibo.cn/comments/hotFlowChild?cid={content_id}&max_id={max_id}&max_id_type=0'
        response = session.get(next_url, headers=headers).json()
        """解析评论内容"""
        self.parse_two_info_response_content(response, content_id)
        """提取翻页的id"""
        max_id = response['max_id']
        print(max_id)
        # time.sleep(random.randint(1, 5))
        """回调解析二级评论内容"""
        self.parse_two_page_response(max_id, content_id, headers)

    def parse_two_info_response_content(self, response, content_id):
        """
        提取二级评论的内容数据
        :param response: 二级评论的响应
        :param content_id: 一级评论的id：表名称
        :return:
        """
        resp_json = response['data']
        for data_response in resp_json:
            text = data_response['text']
            list_2 = [content_id, text]
            data = {
                '二级评论数据': list_2
            }
            self.save_data_to_execl(data)
            # print('二级评论====解析成功====！！！')
        print('=============================翻页中========================================================')

    def save_data_to_execl(self, data):

        os_path_1 = os.getcwd() + '/数据/'
        if not os.path.exists(os_path_1):
            os.mkdir(os_path_1)
        # os_path = os_path_1 + self.os_path_name + '.xls'
        os_path = os_path_1 + '数据.xls'
        if not os.path.exists(os_path):
            # 创建新的workbook（其实就是创建新的excel）
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建新的sheet表
            worksheet1 = workbook.add_sheet("一级评论数据", cell_overwrite_ok=True)
            worksheet2 = workbook.add_sheet("二级评论数据", cell_overwrite_ok=True)
            borders = xlwt.Borders()  # Create Borders
            """定义边框实线"""
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 0x40
            borders.right_colour = 0x40
            borders.top_colour = 0x40
            borders.bottom_colour = 0x40
            style = xlwt.XFStyle()  # Create Style
            style.borders = borders  # Add Borders to Style
            """居中写入设置"""
            al = xlwt.Alignment()
            al.horz = 0x02  # 水平居中
            al.vert = 0x01  # 垂直居中
            style.alignment = al
            # 合并 第0行到第0列 的 第0列到第13列
            '''基本详情13'''
            # worksheet1.write_merge(0, 0, 0, 13, '基本详情', style)
            excel_data_1 = ['评论时间', '评论点赞量', '评论内容', '用户的昵称', '用户的性别', '用户的id', '用户主页地址', '微博认证']
            for i in range(0, len(excel_data_1)):
                worksheet1.col(i).width = 2560 * 3
                #               行，列，  内容，            样式
                worksheet1.write(0, i, excel_data_1[i], style)

            excel_data_2 = ['二级评论id', '二级评论内容']
            for i in range(0, len(excel_data_2)):
                worksheet2.col(i).width = 2560 * 3
                #               行，列，  内容，            样式
                worksheet2.write(0, i, excel_data_2[i], style)
            workbook.save(os_path)
        # 判断工作表是否存在
        if os.path.exists(os_path):
            # 打开工作薄
            workbook = xlrd.open_workbook(os_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_path)


if __name__ == '__main__':
    w = WBSpider()
    w.parse_start_url()
















