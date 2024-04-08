"""
Comment
id      自增变量，创建实例时不需要传入
user_id 评论者的id
comment_time:  评论时间， date类型
reply_to_id:  我的评论回应的comment_id 
content:  评论内容，字符串，长度不定，不可为空
kudo: 收获的赞同数
reply_cnt: 回复我的评论数目
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import inspect

Base = declarative_base()


class Comment(Base):
    __tablename__ = "Comment"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    comment_time = Column(DateTime(), nullable=False)
    reply_to_id = Column(Integer, nullable=False)
    content = Column(String(), nullable=False)
    kudo = Column(Integer, nullable=False)
    reply_cnt = Column(Integer, nullable=False)
 

    def __init__(self, id, user_id, comment_time, reply_to_id, content, kudo, reply_cnt):
        self.id = id
        self.user_id = user_id
        self.comment_time = comment_time
        self.reply_to_id = reply_to_id
        self.content = content
        self.kudo = kudo
        self.reply_cnt = reply_cnt
    

    def __repr__(self):
        return '<Comment %r>' % self.id


"""
在数据库中创建这个表格
先检查是否存在，不存在就创建
"""


def create_comment_table(db):
    Base.metadata.create_all(db.engine)

def drop_comment_table(db):
    Base.metadata.drop_all(db.engine)

def add_comment(db, user_id, comment_time, reply_to_id, content, kudo, reply_cnt):
    if not (user_id and comment_time and reply_to_id and content and kudo and reply_cnt):
        print('Comment info missing.')
        return
    new_comment = Comment(user_id=user_id, comment_time=comment_time, reply_to_id=reply_to_id, content=content,
                          kudo=kudo, reply_cnt=reply_cnt)
    db.session.add(new_comment)
    db.session.commit()

def delete_comment(db, comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()

def modify_comment(db, comment_id, user_id=None, comment_time=None, reply_to_id=None, content=None, kudo=None, reply_cnt=None):
    comment = Comment.query.get(comment_id)
    if comment:
        if user_id is not None:
            comment.user_id = user_id
        if comment_time is not None:
            comment.comment_time = comment_time
        if reply_to_id is not None:
            comment.reply_to_id = reply_to_id
        if content is not None:
            comment.content = content
        if kudo is not None:
            comment.kudo = kudo
        if reply_cnt is not None:
            comment.reply_cnt = reply_cnt
        db.session.commit()

def find_comment_by_id(db, comment_id):
    return Comment.query.get(comment_id)
