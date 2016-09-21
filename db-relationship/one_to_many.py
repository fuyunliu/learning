# -*- coding: utf-8 -*-

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('sqlite:///o2m.db', echo=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()


# the one side
class Parent(Base):
    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # children = relationship("Child", back_populates="parent")
    children = relationship("Child", backref="parent", lazy="dynamic")


# the many side
class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    # parent = relationship("Parent", back_populates="children")
    # parent = relationship("Parent", backref="children")


def init_db():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///o2m.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()


"""
记录backref和back_populates的不同

(1) Parent下添加children = relationship("Child", back_populates="parent")
创建p1 = Parent()和c1 = Child()失败，原因是One or more mappers failed to initialize
即back_populates必须在关系两端同时指定


(2) Parent下添加children = relationship("Child", back_populates="parent")
    Child下添加parent = relationship("Parent", back_populates="children")
Parent Attribute:
Parent.children Parent.id Parent.metadata Parent.name Parent.query

Child Attribute:
Child.id Child.metadata Child.name Child.parent Child.parent_id Child.query

p1 = Parent()
c1 = Child()
c1.parent = p1 or p1.children.append(c1)


(3) Parent下添加children = relationship("Child", backref="parent")
Parent Attribute:
Parent.children Parent.id Parent.metadata Parent.name Parent.query

Child Attribute:
Child.id Child.metadata Child.name Child.parent_id Child.query

p1 = Parent()
c1 = Child()
c1.parent = p1 or p1.children.append(c1)
可以看出使用backref时，实例化c1时会自动在c1对象上添加parent属性
此后再检查:
hasattr(Child, 'parent') // True
hasattr(c1, 'parent') // True
hasattr(Parent, 'children') // True
hasattr(p1, 'children') // True


(4) Child下添加parent = relationship("Parent", backref="children")
情况和(3)相同


(5) Parent下添加children = relationship("Child", backref="parent")
    Child下添加parent = relationship("Parent", backref="children")
创建p1 = Parent()和c1 = Child()失败，原因是One or more mappers failed to initialize
因此两者只能使用其中之一


lazy 指定如何加载相关记录，默认值是"select"
    select 首次访问时按需加载
    immediate 源对象加载后就加载
    joined 加载记录,但使用联结
    subquery 立即加载,但使用子查询
    noload 永不加载
    dynamic 不加载记录,但提供加载记录的查询

lazy = "dynamic"只能用于collections，不立即查询出结果集，而是提供一系列结果集的方法，可以基于结果集再次进行更精确的查找
"""
