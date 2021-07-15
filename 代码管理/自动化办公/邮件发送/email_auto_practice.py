# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
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
# import smtplib
# from email.mime.text import MIMEText   # 邮件正文
# from email.header import Header        # 邮件头部信息
#
# def main():
#     # 1、登录邮箱服务器
#     smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)          # 发件人的SMTP邮件服务器，端口是465,ssl安全协议保护邮件
#     smtp_obj.login('1150772265@qq.com', 'ovluwmfcmoyvgbij')  # 获取动态授权码
#     smtp_obj.set_debuglevel(1)
#
#     # 2、设置邮件内容信息,5部走，内容，内容格式，发送方，接收方，主题
#     msg_content = 'hi, my name is ChenDaXing'
#     message = MIMEText(msg_content, 'plain', 'utf-8')
#     message['From'] = Header('Mr.Chen', 'utf-8')
#     message['To'] = Header('My lover', 'utf-8')
#     message['Subject'] = Header('Please marry me!', 'utf-8')
#
#     # 3、发送邮件
#     sender = '1150772265@qq.com'                #发送方邮箱
#     receiver = ['1150772265@qq.com','1203790708@qq.com']            #接收方邮箱，可多个
#     try:
#         smtp_obj.sendmail(sender, receiver, message.as_string())   # 压缩成字符串格式发送
#         print('***邮件发送成功***')
#     except Exception as e:
#         print('***邮件发送错误***')
#
#
#
#
# if __name__ == '__main__':
#     main()

import smtplib
from email.mime.text import MIMEText   # 邮件正文
from email.header import Header        # 邮件头部信息

def main():
    # 1、登录邮箱服务器
    smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)          # 发件人的SMTP邮件服务器，端口是465,ssl安全协议保护邮件
    smtp_obj.login('1150772265@qq.com', 'ovluwmfcmoyvgbij')  # 获取动态授权码
    smtp_obj.set_debuglevel(1)

    # 2、设置邮件内容信息,5部走，内容，内容格式，发送方，接收方，主题
    msg_content = \
    '''
        <div>
            <h2>WallHaven</h2>
            <p style="font-size: 20px">&emsp;&emsp;&emsp;This is new picture</p>
            &emsp;&emsp;&emsp;<img src="https://w.wallhaven.cc/full/8o/wallhaven-8o3r72.png" alt="图片加载错误">
        </div>
    '''
    message = MIMEText(msg_content, 'html', 'utf-8')
    message['From'] = Header('ChenDaXing', 'utf-8')
    message['To'] = Header('YinYin', 'utf-8')
    message['Subject'] = Header('Halo', 'utf-8')

    # 3、发送邮件
    sender = '1150772265@qq.com'                #发送方邮箱
    receiver = ['1203790708@qq.com','970987676@qq.com']            #接收方邮箱，可多个
    try:
        smtp_obj.sendmail(sender, receiver, message.as_string())   # 压缩成字符串格式发送
        print('***邮件发送成功***')
    except Exception as e:
        print('***邮件发送错误***')




if __name__ == '__main__':
    main()