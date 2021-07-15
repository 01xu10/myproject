# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------


import os, shutil
from pprint import pprint

def main():
    # 1、获取文件路径， 获取文件内容
    file_path = input(r'请输入要整理的文件夹绝对路径：')
    os.chdir(file_path)
    file_names = os.listdir()
    # print(file_names)

    # 2、确定文件后缀
    formats = {
        '音乐': ['.mp3', '.m4a'],
        '视频': ['.mp4', '.avi', 'mkv'],
        '图片': ['.jpg', '.png', '.jepg', '.gif'],
        'word文档': ['.txt', '.doc', '.docx'],
        'ppt文档': ['.ppt'],
        'pdf文档': ['.pdf'],
        'excel文档': ['.xlsx'],
        '程序': ['.exe', '.msi'],
        '压缩': ['.zip', '.rar'],
        '脚本': ['.bat', '.vba']
    }
    # pprint(formats.items())

    # 3、获取文件后缀
    for file_name in file_names:
        file_suffix = os.path.splitext(file_name)[-1].lower()
        # print(file_suffix)

        # 4、获取formats_items
        for file_type, file_suffixs in formats.items():
            if not os.path.isdir(file_type):
                os.mkdir(file_type)
            if file_suffix in file_suffixs:
                shutil.move(file_name, r'{}/{}'.format(file_type, file_name))
    print(r'***文件整理成功***')


if __name__ == '__main__':
    main()
