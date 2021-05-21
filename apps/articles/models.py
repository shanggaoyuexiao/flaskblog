from datetime import datetime
from exts import db


# 文章表
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)  # 文章标题
    content = db.Column(db.TEXT, nullable=False)  # 文章内容
    pdatetime = db.Column(db.DateTime, default=datetime.now)  # 发布时间
    # 和用户id建立外键关系，定义外键是在多的那一方定义的
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    comments = db.relationship('Comment', backref='article')


# 文章分类表
class Article_tepy(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=False)
    articles = db.relationship('Article', backref='type')


# 评论表
'''这是一个多对多建立的第三张表，评论表和用户是一对多，评论表和文章是一对多，这样就实现了评论和用户的多对多。一个文章可以有多个评论，一个用户可以对多个文章评论'''


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    to_id = db.Column(db.String(255))  # 这个表表示回复的是用户的评论
    cdatatime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment
