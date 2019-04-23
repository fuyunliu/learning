# -*- coding: utf-8 -*-

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('sqlite:///m2m.db', echo=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship(
        'Employee',
        secondary='department_employee_link'
    )


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(
        DateTime,
        default=func.now())
    departments = relationship(
        'Department',
        secondary='department_employee_link'
    )


class DepartmentEmployeeLink(Base):
    __tablename__ = 'department_employee_link'
    department_id = Column(Integer, ForeignKey('department.id'),
                           primary_key=True)
    department = relationship('Department')
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    employee = relationship('Employee')


def init_db():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///m2m.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()


"""
在sqlalchemy中为DateTime类型的字段设置默认值时的建议：
1, DateTime类型的字段值最好让数据库自己计算，而不是程序
2, 为字段设置默认值时一般用server_default比default更好
3, sqlalchemy有func.now()和func.current_timestamp()来告诉数据库自己计算时间戳
4, 注意func.now() 和 func.current_timestamp()均返回的是函数
5, sqlalchemy中的onupdate意味着当记录更新时，该字段会更新为一个新的时间戳
6, server_default是在数据库层设置默认值，default是在使用sqlalchemy时在python层设置默认值
举个例子：
from sqlalchemy.sql import func
time_created = Column(DateTime(timezone=True), server_default=func.now())
time_updated = Column(DateTime(timezone=True), onupdate=func.now())

在flask中可以使用
from datetime import datetime
time_created = Column(DateTime(timezone=True), server_default=datetime.utcnow)
time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)

在django中可以使用
from django.utils import timezone
time_created = Column(DateTime(timezone=True), server_default=timezone.now)
time_updated = Column(DateTime(timezone=True), onupdate=timezone.now)

"""
