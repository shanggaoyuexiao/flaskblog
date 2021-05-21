from flask import render_template, request, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps import create_app
from apps.user.models import *
from apps.articles.models import *

# 创建app对象，注意app对象是一个核心
from exts import db

app = create_app()
manager = Manager(app=app)  # 把app用manager包裹起来，这是连接数据库的第一步
migrate = Migrate(app=app, db=db)  # 这句话先是让数据库命令migrate和app,db联系
# 最后把数据库的命令加到manager中去
manager.add_command('db', MigrateCommand)

#主页
@app.route('/')
def index():
    # print(111111111)
    # print(request.host)       #获取ip地址
    # 获取uid是用户的id
    # uid=request.cookies.get('uid',None)     #注意这里的uid是一个字符串类型的数字
    # session的获取方式
    uid = session.get('uid')  # 这里的uid是从用户登录那里拿到的字符串类型的用户主键
    # 获取文章列表,这里要获取文章列表的反序，所以要查询前面要加一个杠
    articles = Article.query.order_by(-Article.pdatetime).all()
    # 获取分类列表
    types = Article_tepy.query.all()
    if uid:
        # 这句话的意思是根据字符串类型的数字uid，找到用户对象.
        user = User.query.get(uid)
        return render_template('base.html', user=user, articles=articles, types=types)  # 拿到用户对象，然后渲染到页面base
    else:
        return render_template('base.html', articles=articles, types=types)


if __name__ == '__main__':
    manager.run()
