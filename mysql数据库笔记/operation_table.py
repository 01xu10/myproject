# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_db import Depart, User

# 1、连接数据库
engine = create_engine(
    "mysql+pymysql://mysql:qwe123@localhost/Python_12?charset=utf8", echo=True, pool_size=5, max_overflow=5
)

# 2、创建session
DBsession = sessionmaker(bind=engine)
session = DBsession()

''' 增加操作 '''
# 添加部门数据
part_1 = Depart(0, '财务部')
part_2=  Depart(0, '商务部')
part_3 = Depart(0, '信贷部')
session.add_all([part_1, part_2, part_3])
print('成功添加部门信息')

# 添加员工数据
user1 = User(0, '张三', 19, '女', '13811111', 1)
user2 = User(0, '李四', 20, '男', '13822222', 3)
user3 = User(0, '王五', 30, '女', '13833333', 3)
user4 = User(0, '赵六', 29, '男', '13844444', 2)
user5 = User(0, '孙七', 20, '女', '13855555', 3)
user6 = User(0, '许八', 20, '男', '13866666', 1)
user7 = User(0, '刘九', 21, '男', '13877777', 1)
user8 = User(0, '楚十', 36, '男', '13888888', 2)
session.add_all([user1,user2,user3,user4,user5,user6,user7,user8])
print('成功添加员工信息')


'''查询操作'''
# A、查询所有员工的编号，姓名，所属部门编号
query_user_obj = session.query(User).all()
for user in query_user_obj:
    print(user.id, user.name, user.depart_id)


# B、查询所有部门编号为2的员工信息
'''filter_by 查询'''
query_user_obj = session.query(User).filter_by(depart_id=2).all()
for user in query_user_obj:
    print(user.id, user.name, user.depart_id)


'''filter 查询'''
query_user_obj = session.query(User).filter(User.depart_id == 2).all()
for user in query_user_obj:
    print(user.id, user.name, user.depart_id)


# 查询年龄为在 19 ~ 29的员工信息，并按年龄大小排序， 升序 --> asc()，降序 --> desc()
query_user_obj = session.query(User).filter(User.age.between(19, 29)).order_by(User.age.asc()).all()
for user in query_user_obj:
    print(user.id, user.name, user.age)


# 查询部门编号为 1，年龄大于 20的员工信息
query_user_obj = session.query(User, Depart).join(Depart).filter(User.age>20, Depart.id==1).all()
for (user,department) in query_user_obj:
    print(user.id, user.name, user.age, department.name)


''' 删除操作 '''
# 1、删除名字等于楚十的员工信息(返回一个整数，代表操作的数据条数) --> filter
session.query(User).filter(User.name == '楚十').delete()

# 2、删除电话等于13844444的信息(返回一个整数，代表操作的数据条数) --> filter_by
res = session.query(User).filter_by(phone = '13855555').delete()
print(type(res))

# 2、删除年龄等于20的员工信息
delete_user_obj = session.query(User).filter(User.age == 20).delete()
print(delete_user_obj)

# 3、删除部门为 3的所有员工信息
res = session.query(Depart).filter_by(id = 2).delete()
print(res)

# 4、删除员工信息表(返回一个整数，代表操作的数据条数)
delete_user_table = session.query(User).delete()
print(delete_user_table)


''' 修改操作 '''
# 将用户信息表中的 id=1001的用户的姓名改成 Jack (返回一个整数，代表操作的数据条数)
update_user = session.query(User).filter_by(id = 1001).update({'name': '张三', 'age': 37})
print(update_user)


# session 的提交和关闭
session.commit()
session.close()
