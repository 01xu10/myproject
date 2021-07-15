"""
微博评论爬虫：
需求：爬微博评论区用户评论内容，评论时间，点赞数，用户名，用户id，用户性别，用户地区，用户微博数，用户粉丝数，用户关注数
excel 格式保存
10
"""
"""
解析步骤：
    1.解析用户评论内容，评论时间，点赞数，用户名，用户id
        1.进入手机模式
        2.找到相关微博正文
        3.点击评论，查看更多，跳转到微博正文详情页
        4.翻页，下一页的max_id来自于上一页的响应中
          也就是说，第二页的max_id在第一页的响应中
          
    2.解析用户性别，用户地区，用户微博数，用户粉丝数，用户关注数
        1.通过抓包分析，得
            https://m.weibo.cn/api/container/getIndex?type=uid&value=1669879400
        这条url地址得背后就是需求得用户微博主页数据
            对应的
            https://m.weibo.cn/api/container/getIndex?type=uid&value= + 微博id
"""
from requests_html import HTMLSession
from xlutils.copy import copy
import os, xlrd, xlwt, re, datetime
session = HTMLSession()


class WbSpider(object):
    def __init__(self):
        # 微博起始url地址
        self.start_url = 'https://m.weibo.cn/comments/hotflow?id=4587934706048164&mid=4587934706048164&max_id_type=0'

    def parse_start_url(self):
        """
        解析微博正文评论第一部分数据
        :return:
        """
        # 单独构造请求头
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': '4e1e49',
            'referer': 'https://m.weibo.cn/status/JATAapnp2?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'cookie': 'WEIBOCN_FROM=1110005030; loginScene=102003; SUB=_2A25NH_02DeRhGeFL61AR8SrEzTyIHXVu44N-rDV6PUJbkdAKLWbfkW1NQrcPFF8wkqqh9Jxna86_WE0mhzVt6FOV; _T_WM=97902222169; XSRF-TOKEN=260df0; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4587934706048164%26luicode%3D20000061%26lfid%3D4587934706048164%26uicode%3D20000061%26fid%3D4587934706048164'}
        # 发送请求，获取响应
        response = session.get(self.start_url, headers=headers)
        if response.status_code == 200:
            """调用解析微博正文评论json数据方法"""
            self.parse_comment_resp_json(response.json())
            """开始翻页"""
            try:
                data = response.json()
                # 解析下一页翻页的max_id
                max_id = data['data']['max_id']
                # 假如说最后一页的max_id 为空
                self.parse_comment_page(max_id)
            except:
                self.parse_start_url()
        else:
            print('访问失败，请加入代理替换cookie')
            self.parse_start_url()

    def parse_comment_resp_json(self, response_json):
        """
        解析微博正文评论json数据方法，通用
        :param response_json: 响应的json数据
        :return:
        """
        # 解析微博正文第一页评论
        comment_data = response_json['data']['data']
        # for 循环遍历取出每一条评论相关数据
        for comment in comment_data:
            # 评论内容
            comment_content_str = comment['text']
            try:
                # 正则匹配有表情的评论内容，匹配出表情主题
                content_str = re.findall(r'alt=(.*?) ', comment_content_str)[0]
                # 正则sub匹配，将表情标签替换为表情主题
                comment_content = re.sub("<span(.*?)</span>", content_str, comment_content_str)
            except:
                # 正则匹配失败会报错，代表评论内容无表情，在此使用try
                comment_content = comment_content_str
            # 评论时间
            comment_time = comment['created_at']
            # 定义转换格式
            time_format = '%a %b %d %H:%M:%S %z %Y'
            # 格式化时间
            comment_time = str(datetime.datetime.strptime(comment_time, time_format))
            # 点赞数
            give_z = comment['like_count']
            # 用户名
            user_name = comment['user']['screen_name']
            # 用户id
            user_id = comment['user']['id']
            comment_list = [comment_content, comment_time, give_z, user_name, user_id]
            """调用解析微博主页数据方法"""
            self.parse_user_html(user_id, comment_list)

    def parse_comment_page(self, max_id):
        """
        解析微博正文评论翻页处理
        :param max_id: 下一页的max_id
        :return:
        """
        print('开始翻页----longing----！！！')
        next_url = f'https://m.weibo.cn/comments/hotflow?id=4587934706048164&mid=4587934706048164&max_id={max_id}&max_id_type=0'
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': '4e1e49',
            'referer': 'https://m.weibo.cn/status/JATAapnp2?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'cookie': 'WEIBOCN_FROM=1110005030; loginScene=102003; SUB=_2A25NHumrDeRhGeFL61AR8SrEzTyIHXVu4PfjrDV6PUJbkdAKLXjQkW1NQrcPFGEk2Z8xZ1HU9pQ83mM4ys0JshTD; _T_WM=96715018363; XSRF-TOKEN=4e1e49; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4587934706048164%26luicode%3D20000061%26lfid%3D4587934706048164%26uicode%3D20000061%26fid%3D4587934706048164'
        }
        response = session.get(next_url, headers=headers)
        if response.status_code == 200:
            """调用解析微博正文评论json数据方法"""
            self.parse_comment_resp_json(response.json())
            try:
                data = response.json()
                # 解析下一页翻页的max_id
                max_id = data['data']['max_id']
                # 假如说最后一页的max_id 为空
                self.parse_comment_page(max_id)
            except:
                self.parse_comment_page(max_id)
        else:
            print('访问失败，请加入代理替换cookie')
            self.parse_comment_page(max_id)

    def parse_user_html(self, user_id, comment_list):
        """
        解析微博主页数据
        :param user_id: 用户id
        :param comment_list: 部分需求数据
        :return:
        """
        wb_url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36'
        }
        response = session.get(wb_url, headers=headers)
        if response.status_code == 200:
            data_json = response.json()
            try:
                # 用户性别
                user_sex = data_json['data']['userInfo']['gender']
                user_sex = '女' if user_sex == 'f' else '男'
                # if user_sex == 'f':
                #     user_sex = '女'
                # else:
                #     user_sex = '男'
                comment_list.append(user_sex)
            except:
                self.parse_user_html(user_id, comment_list)
            # 用户地区
            user_addr = data_json['data']['userInfo']['description']
            comment_list.append(user_addr)
            # 用户微博数
            user_num = data_json['data']['userInfo']['statuses_count']
            comment_list.append(user_num)
            # 用户粉丝数
            user_fans = data_json['data']['userInfo']['followers_count']
            comment_list.append(user_fans)
            # 用户关注数
            user_attention = data_json['data']['userInfo']['follow_count']
            comment_list.append(user_attention)
            self.save_data(comment_list)
        else:
            print('访问失败，请加入代理替换cookie')
            self.parse_user_html(user_id, comment_list)

    def save_data(self, data):
        """
        保存到excel表格
        :param data: 需要保存的数据
        :return:
        """
        os_path_1 = os.getcwd() + '/数据/'
        if not os.path.exists(os_path_1):
            os.mkdir(os_path_1)
        # os_path = os_path_1 + self.os_path_name + '.xls'
        os_path = os_path_1 + '数据.xls'
        if not os.path.exists(os_path):
            # 创建新的workbook（其实就是创建新的excel）
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建新的sheet表
            worksheet1 = workbook.add_sheet("基本详情", cell_overwrite_ok=True)
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
            excel_data_1 = ('评论内容', '评论时间', '点赞数', '用户名', '用户id', '用户性别', '个性描述',
                            '用户微博数', '用户粉丝数', '用户关注数')
            for i in range(0, len(excel_data_1)):
                worksheet1.col(i).width = 2560 * 3
                #               行，列，  内容，            样式
                worksheet1.write(0, i, excel_data_1[i], style)
            workbook.save(os_path)

        # 判断工作表是否存在
        if os.path.exists(os_path):
            # 打开工作薄
            workbook = xlrd.open_workbook(os_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                worksheet = workbook.sheet_by_name(sheets[i])
                # 获取工作薄中所有表中的表名与数据名对比
                # 获取表中已存在的行数
                rows_old = worksheet.nrows
                # 将xlrd对象拷贝转化为xlwt对象
                new_workbook = copy(workbook)
                # 获取转化后的工作薄中的第i张表
                new_worksheet = new_workbook.get_sheet(i)
                for num in range(0, len(data)):
                    new_worksheet.write(rows_old, num, data[num])
                new_workbook.save(os_path)
                print('表格写入成功----logging----！！！')


if __name__ == '__main__':
    wb = WbSpider()
    wb.parse_start_url()
