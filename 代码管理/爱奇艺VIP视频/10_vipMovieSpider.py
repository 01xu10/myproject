# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

from urllib import parse
import re, webbrowser, tkinter as tk
import tkinter.messagebox as msgbox


class App(object):
    def __init__(self):
        # 1、设置窗口大小
        self.width = 1000
        self.height = 600
        # 2、GUI名称
        self.title = '视频解析助手 - Vce'
        # 3、创建一个tk对象
        self.root = tk.Tk(className = self.title)
        # 4、用户输入的url值，通过类属性接收
        self.url = tk.StringVar()
        # 5、声明解析通道为默认通道
        self.value = tk.IntVar()
        self.value.set(1)
        # 6、创建界面空间布局对象
        frame_title = tk.Frame(self.root)
        frame_body = tk.Frame(self.root)
        # 7、软件空间内容布局 -- 标题部分
        group = tk.Label(frame_title, text='播放通道', padx=10, pady=10)
        tb = tk.Radiobutton(frame_title, text='唯一通道', variable=self.value, value=1, width=10, height=3)
        # 8、软件空间内容布局 -- 主体部分
        label = tk.Label(frame_body, text='请输入视频播放的视频地址：')
        entry = tk.Entry(frame_body, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=40)
        play = tk.Button(frame_body, text='播放', font=('微软雅黑', 12), fg='Purple', width=2, height=1, command=self.video_play)
        # 9、激活软件空间
        frame_title.pack()
        frame_body.pack()
        # 10、控件位置布局  -- 标题部分
        group.grid(row=0, column=0)
        tb.grid(row=0, column=1)
        # 11、控件位置布局  -- 主体部分
        label.grid(row=0, column=0)
        entry.grid(row=0, column=0)
        play.grid(row=0, column=2, ipadx=10, ipady=10)

    def video_play(self):
        # 视频API接口
        wmxz_url = r'http://www.wmxz.wang/video.php?url='
        if re.match(r'https?:/{2}\w.+$', self.url.get()):
            start_url = self.url.get()
            start_url = parse.quote_plus(start_url)
            webbrowser.open(wmxz_url + start_url)
        else:
            msgbox.showerror(title='错误', message='视频地址无效，请重新输入')


    def loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.loop()
