from flask import Flask
import settings
from apps.articles.views import article_bp
from apps.user.views import user_bp
from exts import db, bootstrap


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # app是一个核心对象
    app.config.from_object(settings.DevelopmentConfig)
    # 注册蓝图
    app.register_blueprint(article_bp)
    app.register_blueprint(user_bp)
    # 连接数据库，1首先让db和app联系
    db.init_app(app=app)
    bootstrap.init_app(app=app)  # bootstrap和app联系

    return app
