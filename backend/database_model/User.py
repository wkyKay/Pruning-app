"""
User
id      自增变量，创建实例时不需要传入
username:   字符串，长度不定，不可为空
password:   字符串，长度不定，不可为空
avatar:  头像，字符串
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import inspect

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    avatar = Column(BYTEA, nullable=True)
 

    def __init__(self, id, username, password, avatar):
        self.id = id
        self.username = username
        self.password = password
        self.avatar = avatar
    

    def __repr__(self):
        return '<User %r>' % self.username


def create_user_table(db):
    Base.metadata.create_all(db.engine)

def drop_user_table(db):
    Base.metadata.drop_all(db.engine)

def add_user(db, username, password, avatar):
    if not (username and password):  # 检查用户名和密码是否为空
        print('Username or password cannot be empty.')
        return
    new_user = User(username=username, password=password, avatar=avatar)
    db.session.add(new_user)
    db.session.commit()

def delete_user(db, username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()

def modify_user(db, user_id, username=None, password=None, avatar=None):
    user = User.query.get(user_id)
    if user:
        if username:
            user.username = username
        if password:
            user.password = password
        if avatar:
            user.avatar = avatar
        db.session.commit()

def find_user_by_id(db, user_id):
    return User.query.get(user_id)
