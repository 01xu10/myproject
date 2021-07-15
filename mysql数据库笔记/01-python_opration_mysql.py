# !/usr/bin/env python
# encoding: utf-8
# ------------------------------
# @project : 数据库基础
# @File    : Python 操作 MySQL.py
# @Software: PyCharm
# @Author  :  Vce
# @Time    : 2020/2/23 12:40
# ------------------------------

import pymysql

# 1、建立连接
db_config = {
    'user': 'mysql',
    'password': 'qwe123',
    'db': 'Python_vce',
    'charset': 'utf8',
}
conn = pymysql.connect(**db_config)

# 2、创建 cursor
cur = conn.cursor()

# 3、执行 MySQL语句，cur.execute(......)    # 插入数据，默认进入事物模式
cur.execute('select * from student')          # 返回的是生效行数

conn.commit()

print(cur.fetchone())                       # 每次运行返回一条数据
print(cur.fetchall())                       # 返回所有数据    (一般不使用，因为可能造成内存不足)
print(cur.fetchmany(5))                     # 返回指定条数据( 示例为5条 )

# 返回所有数据 (使用变量row，不占内存，每条row数据，会被后面的相应覆盖)：
row = cur.fetchone()
while row:
    print(row)
    row = cur.fetchone()

# 4、关闭 cursor
cur.close()

# 5、关闭连接
conn.close()

# 6、事物的回滚和提交
# 进入事物 ：begin ；                数据只是暂时写进去，需要进行提交操作后，才真正把数据写进表格
# 回滚    ： rollback；              如果数据写错了，使用回滚 (每次混滚后，需要重进事物)
# 提交    ： commit；                提交后，数据写入表格

# 7、上下文管理       with ... as...

# 8、 将 MySQL 方法封装成类
import pymysql

class MySql:
    def __init__(self):
        db_config = {
            'user': 'root',
            'password': 'qwe123',
            'db': 'Python_vce',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**db_config)
        self.cur = self.conn.cursor()

    def insert(self, db_name, *args):
        args = list(args)
        for i in range(len(args)):
            args[i] = tuple(args[i])
        args = str(args)
        data = args[1:-1]
        sql = f"insert into {db_name} values {data}"
        print(sql)
        self.cur.execute(sql)

    def find(self, db_name):
        self.cur.execute(f'select * from {db_name}')
        data = self.cur.fetchone()
        while data:
            print(data)
            data = self.cur.fetchone()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.cur.close()


# 对象实例化
Vce = MySql()

# 插入数据
Vce.insert('student', [16,'Math','boy',10,3],[19, 'LY', 'girl', 18, 1])
# 查看数据
Vce.find('student')
# 关闭
Vce.close()



# 9、 pymysql操作
import pymysql
db_config = {
    'user': 'root',
    'password': 'qwe123',
    'db': 'Python_vce',
    'charset': 'utf8'
}
conn = pymysql.connect(**db_config)

with conn.cursor() as cur:
    # 插入数据
    cur.execute("insert into student values(100,'China','boy','10',3)")
    # 删除数据
    cur.execute("delete from student where name = 'China'")
    # 更改数据
    cur.execute("update student set sex = 'girl' where class = 3 ")
    # 查看数据
    cur.execute("select * from student")
    data = cur.fetchone()
    while data:
        print(data)
        data = cur.fetchone()
# 提交
conn.commit()
# 回滚
conn.rollback()


# 10、把mysql数据表插入一万条数据，自己定义表结构。
import pymysql

db_config = {
    'user': 'root',
    'password': 'qwe123',
    'db': 'Python_vce',
    'charset': 'utf8'
}
conn = pymysql.connect(**db_config)
cur = conn.cursor()

cur.execute('select * from student')
data = cur.fetchone()
while data:
    print(data)
    data = cur.fetchone()























