from requests_html import HTMLSession
from fake_useragent import UserAgent
import tkinter.messagebox as msgbox
import tkinter as tk
import webbrowser
import os, re, time, random


class BXSpider(object):
    ua = UserAgent()
    session = HTMLSession()

    def __init__(self):
        """
        控制面板配置
        """
        self.width = 800
        self.height = 800
        self.title = '百姓网助手'
        self.root = tk.Tk(className=self.title)
        # 定义button控件上的文字
        self.url = tk.StringVar()
        # 定义选择哪个大分类
        self.v = tk.IntVar()
        # 默认为0
        self.v.set(0)
        # Frame空间
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)
        frame_3 = tk.Frame(self.root)
        # Menu菜单
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        movie_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='友情链接', menu=movie_menu)
        # 获取标题
        url = 'https://luoyuan.baixing.com/'
        response = self.session.get(url)
        self.name_list = response.html.xpath("//div[@class='container nav']/ul/li/a/text()")
        self.url_list = response.html.xpath("//div[@class='container nav']/ul/li/a/@href")
        # 各个网站链接
        movie_menu.add_command(label='百姓网', command=lambda: webbrowser.open('https://luoyuan.baixing.com/'))
        # 控件内容设置
        group = tk.Label(frame_1, text='频道:', padx=20, pady=20)
        # 动态命名接收动态变量
        tb = locals()
        for num in range(len(self.name_list)):
            tb['tb' + str(num)] = tk.Radiobutton(frame_1, text=self.name_list[num], variable=self.v, value=num,
                                                 width=10, height=3)
        label1 = tk.Label(frame_2, text="请输入登录之后的用户cookie：")
        entry = tk.Entry(frame_2, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=35)
        label2 = tk.Label(frame_2, text=" ")
        play = tk.Button(frame_2, text="查询", font=('楷体', 12), fg='Purple', width=2, height=1,
                         command=self.method_classify)
        label3 = tk.Label(frame_2, text=" ")
        label_explain = tk.Label(frame_3, fg='red', font=('楷体', 12),
                                 text='\n使用说明：cookie的获得方法\n在帐号登录之后，右击检查，点击network，刷新页面\n'
                                      '点击一个请求包，点击headers，找到request headers 对着cookie复制即可，粘贴在输入框中'
                                      '\n操作完成，点击“查询”按钮即可')
        label_warning = tk.Label(frame_3, fg='blue', font=('楷体', 12), text='\n程序会自行创建保存文件夹，建议放在桌面运行\n')
        # 控件布局
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        group.grid(row=0, column=0)
        for num in range(len(self.name_list)):
            tb['tb' + str(num)].grid(row=0, column=num)
        label1.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        label2.grid(row=0, column=2)
        play.grid(row=0, column=3, ipadx=10, ipady=10)
        label3.grid(row=0, column=4)
        label_explain.grid(row=1, column=0)
        label_warning.grid(row=2, column=0)

    def method_classify(self):
        """
        行为分类
        :return:
        """
        cookie = self.url.get()
        """提取cookie"""
        if cookie is '':
            cookie = '__trackId=157277922761229; __admx_track_id=XxWYbFf0F81Zd2KwqkVBbA; __admx_track_id.sig=jOK9ti9YtA3mCEPyLsdyd3kYUnM; _ga=GA1.2.647890989.1572779228; _gid=GA1.2.1349886581.1616154397; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1616051394,1616154397; hide_gongzuo_bottom_board=1; __uuid=116161607707397.986d9; login_on_tab=0; __s=kr8pqnc205deo6nnd70rchdur6; __city=changsha; mc=0%2C0%2C0; __chat_udid=bae612af-bf29-427a-b9e4-fec65d52e60d; appId=8brlm7ufr6863; rongSDK=websocket; u237906657_4e200cc207595u237906657_4e200cc207595=1616083200000; __area2=luoyuan; _gat=1; __t=ut6054a8282c55a7.85144865; __u=237906657; __c=3f5e8d7b4ff5f537bdbd0a018cbc96b29ad2a289; __n=%E5%B0%8F%E7%99%BE%E5%A7%9303192103073; __m=16607440667; mui=https%3A%2F%2Fimg4.baixing.net%2F9cbabfa17f95d1495eeeb6b1ebce0581.png_sqwbp; agreedUserPrivacy=1; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1616162397; __sense_session_pv=46; navi9b99cb53=ws72.cn.ronghub.com:443,u237906657_4e200cc207595'
        """解析分类"""
        url = self.url_list[self.v.get()]
        self.parse_start_url(url, cookie)

    def parse_start_url(self, url, cookie):
        """
        解析分类方法，根据用户选择得分类进行查询
        :param url: 用户选择得分类
        :param cookie: 用户登录之后的cookie
        :return:
        """
        headers = {
            'user-agent': self.ua.chrome
        }
        try:
            job_id = re.findall(r'/(.*?)/', url)[0]
        except:
            job_id = ''
        for page in range(1, 100):
            url = 'https://luoyuan.baixing.com/' + job_id + f'?page={page}'
            response = self.session.get(url, headers=headers)
            if response.status_code != 200:
                msgbox.showerror(title=response.status_code, message=f'出现{response.status_code}, 请等会儿重试,记得更新cookie')
            """解析工作列表页"""

            job_url_list = response.html.xpath("//div[@class='main']/ul/li/a/@href")
            """遍历取出列表页数据"""
            time.sleep(random.randint(1, 3))
            for start_url in job_url_list:
                self.parse_job_url(start_url, cookie)
                break
            break

    def parse_job_url(self, start_url, cookie):
        """
        解析工作详情页
        :param start_url: 工作详情页url地址
        :param cookie: 用户登录之后的cookie
        :return:
        """
        headers = {
            'user-agent': self.ua.chrome,
            'cookie': cookie
        }
        response = self.session.get(start_url, headers=headers)
        print(response.content.decode())

    def parse_data(self, data):
        """
        解析data数据，数据提取
        :param data: 响应的源码数据
        :return:
        """

        pass

    def run(self):
        """
        窗口居中
        :return:
        """
        self.root.mainloop()


if __name__ == '__main__':
    b = BXSpider()
    b.run()









