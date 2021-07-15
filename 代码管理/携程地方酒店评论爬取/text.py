# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : text.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/22 16:42
# ------------------------------

import js2py

js = js2py.EvalJs()
with open('xiecheng_houtel_id.js', 'r')as f:
    js.execute(f.read())
    r = js.gencb()
print(r)