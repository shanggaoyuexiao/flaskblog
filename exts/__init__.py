from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#建立与数据库的映射
db=SQLAlchemy()
#使用bootstrap
bootstrap=Bootstrap()       #这2个第三方扩展都要和app连接起来，在工厂函数里