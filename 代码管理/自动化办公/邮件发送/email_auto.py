# !/usr/bin/env python
# -*- coding: utf-8 -*-


'''
    1、邮件处理模块，smtplib

    2、SMTP(Simple Mail Transfer Protocol): 简单邮件传输协议，是一组用于由源地址到目的地址传送邮件的规则，用它来控制中转方式。

    3、实现邮件发送需要满足的条件：
        A、登录邮件服务器;        --> smtplib
        B、构造合法的邮件内容;    --> email
        C、发送邮件！             --> smtplib

    4、Python对SMTP支持有smtplib和email两个模块
        A、email   ：负责构造邮件;
        B、smtplib ：负责发送邮件;
'''


'''
    5、实现一个简单的邮件发送！
'''
import smtplib
from email.mime.text import MIMEText   # 邮件正文
from email.header import Header        # 邮件头部信息

def main():
    # 1、登录邮箱服务器
    smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)               # 发件人的SMTP邮件服务器，端口是465
    smtp_obj.login('', 'ovluwmfcmoyvgbij')        # 获取动态授权码
    smtp_obj.set_debuglevel(1)                                    # 显示调试信息

    # 2、设置邮件内容信息
    msg_content = 'Hello, 小哥哥, 约吗？800上门, 新到学生妹...=.='
    message = MIMEText(msg_content, 'plain', 'utf-8')            # 邮件正文，使用plain格式发送
    message['From'] = Header('Vce', 'utf-8')                     # 邮件头：接收者信息
    message['To'] = Header('女神', 'utf-8')                      # 邮件头：接收者信息
    message['Subject'] = Header('来自贝塔的爱情', 'utf-8')          # 邮件头：邮件主题信息

    # 3、发送邮件
    sender = '@qq.com'                                   # 发送者邮箱
    receiver = ['@qq.com']                              # 接受者邮箱
    smtp_obj.sendmail(sender, receiver, message.as_string())      # 压缩成字符串格式发送


if __name__ == '__main__':
    main()



'''
    6、实现一个带图片的html的邮件发送！
'''
import smtplib
from email.mime.text import MIMEText   # 邮件正文
from email.header import Header        # 邮件头部信息

def main():
    # 1、登录邮箱服务器
    smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)               # 发件人的SMTP邮件服务器，端口是465
    smtp_obj.login('@qq.com', '')        # 获取动态授权码
    smtp_obj.set_debuglevel(1)                                    # 显示调试信息

    # 2、设置邮件内容信息
    msg_content = \
        '''
            <div>
                <h2>贝塔哥哥</h2>
                <p style="font-size: 20px">&emsp;&emsp;&emsp;你好，小哥哥，约吗？只要800，新到学生妹...=.=</p>
                <p style="font-size: 20px">&emsp;&emsp;&emsp;小哥哥,这就是我的样子哦！=.=</p>
                &emsp;&emsp;&emsp;<img src="https://img.tupianzj.com/uploads/allimg/202010/9999/0599b3be86.jpg" alt="图片加载错误"
                   style="width: 400px" height="500px">
            </div>
        '''
    message = MIMEText(msg_content, 'html', 'utf-8')             # 邮件正文，使用html格式发送
    message['From'] = Header('Vce', 'utf-8')                     # 邮件头：发送者信息
    message['To'] = Header('女神', 'utf-8')                      # 邮件头：接收者信息
    message['Subject'] = Header('来自贝塔的爱', 'utf-8')          # 邮件头：邮件主题信息

    # 3、发送邮件
    sender = '@qq.com'                                   # 发送者邮箱
    receiver = ['@qq.com']                              # 接受者邮箱
    smtp_obj.sendmail(sender, receiver, message.as_string())      # 压缩成字符串格式发送


if __name__ == '__main__':
    main()


