"""
该窗体界面拓展性高
具体更改流程如下：

1.将用户名可替换为爬虫检索用户输入的关键词输入

2.密码可替换为账号登录的cookie输入

3.Text富文本框该位置课选择输出爬虫效果print内容

4.对比事件绑定方法借鉴，即可创建程序执行关联函数

"""

import tkinter as tk


class TKSpider(object):

    def __init__(self):
        """定义可视化窗口，并设置窗口和主题大小布局"""
        self.window = tk.Tk()
        self.window.title('阿尔法数据采集')
        self.window.geometry('800x600')

        """创建label_user按钮，与说明书"""
        self.label_user = tk.Label(self.window, text='用户名：', font=('Arial', 12), width=30, height=2)
        self.label_user.pack()
        """创建label_user关联输入"""
        self.entry_user = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_user.pack(after=self.label_user)

        """创建label_passwd按钮，与说明书"""
        self.label_passwd = tk.Label(self.window, text="密码：", font=('Arial', 12), width=30, height=2)
        self.label_passwd.pack()
        """创建label_passwd关联输入"""
        self.entry_passwd = tk.Entry(self.window, show='*', font=('Arial', 14))  # 显示成密文形式
        self.entry_passwd.pack(after=self.label_passwd)

        """创建Text富文本框，用于按钮操作结果的展示"""
        self.text1 = tk.Text(self.window, font=('Arial', 12), width=50, height=5)
        self.text1.pack()

        """定义按钮1，绑定触发事件方法"""
        """即登录按钮，当点击时将执行parse_hit_click_1方法。在真实使用场景中"""
        """parse_hit_click_1中可替换为自己写的真正登录函数。这里仅为示例"""
        self.button_1 = tk.Button(self.window, text='登录', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_1)
        self.button_1.pack(before=self.text1)

        """定义按钮2，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='清除', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_2)
        self.button_2.pack(anchor="e")

    def parse_hit_click_1(self):
        """定义触发事件1, 将执行结果显示在文本框中"""
        printinfo = "您输入的用户名是{},密码是{}".format(self.entry_user.get(), self.entry_passwd.get())
        self.text1.insert("insert", printinfo + "\n")

    def parse_hit_click_2(self):
        """定义触发事件2，删除文本框中内容"""
        self.entry_user.delete(0, "end")
        self.entry_passwd.delete(0, "end")
        self.text1.delete("1.0", "end")

    def center(self):
        """创建窗口居中函数方法"""
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (800 / 2))
        y = int((hs / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(800, 600, x, y))

    def run_loop(self):
        """禁止修改窗体大小规格"""
        self.window.resizable(False, False)
        """窗口居中"""
        self.center()
        """窗口维持--持久化"""
        self.window.mainloop()


if __name__ == '__main__':
    t = TKSpider()
    t.run_loop()










