from datetime import datetime
from exts import db

'''做一个项目前首先要确定建立的表，然后在确定他们之间的关系，博客最重要的就是文章，用户，和评论'''


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 这表示主键自增
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)  # 默认删除
    rdatetime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    '''relationship()作用是在view和template中体现的(模板上传递的是用户的信息，我们要根据用户的信息拿到文章的),第一个参数是你要找的是谁,第二个参数是方向引用
       relationship()的作用就是快速简单实现表连接查询的，一对多实际的作用就是根据一个用户可以找到此用户其他的信息，但是不能通过其他用户找到其他用户的相关信息
       而多对多。多对多要建立第三张表，第三张表分别和多对多的两张表是一对多的关系'''
    articles = db.relationship('Article', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __str__(self):
        return self.username


# ip表
class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)


# 图片
class Phote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(50), nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.photo_name
