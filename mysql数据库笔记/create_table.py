# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Date, DateTime

# 创建对象的基类
Base = declarative_base()

# 链接数据库
engine = create_engine(
    "mysql+pymysql://mysql:qwe123@localhost/Python_12?charset=utf8", echo=True, pool_size=5, max_overflow=5
)


# 部门表
class Depart(Base):
    __tablename__ = "depart"

    id = Column(Integer, primary_key=True, autoincrement=True, doc='编号')
    name = Column(String(20), unique=True, doc='名称')

    def __init__(self, id, name):
        self.id = id
        self.name = name


# 员工表
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, doc='编号')
    name = Column(String(20), doc='名称')
    age = Column(Integer, doc='年龄')
    gender = Column(Enum('男', '女'), default='男', doc='性别')
    phone = Column(String(11), doc='电话')

    depart_id = Column(Integer, ForeignKey('depart.id'), doc='绑定部门id')

    def __init__(self, id, name, age, gender, phone, depart_id):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self. depart_id = depart_id


if __name__ == '__main__':
    Base.metadata.create_all(engine)

