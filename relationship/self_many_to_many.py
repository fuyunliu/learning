# -*- coding: utf-8 -*-

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('sqlite:///selfm2m.db', echo=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()


class Follow(Base):
    __tablename__ = 'follows'
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    followed = relationship('Follow',
                            backref='follower',
                            primaryjoin=id == Follow.followed_id)
    followers = relationship('Follow',
                             backref='followed',
                             primaryjoin=id == Follow.follower_id)


def init_db():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///selfm2m.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
