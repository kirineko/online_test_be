from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import config

db = SQLAlchemy()
admin = Admin(name='在线测试小程序管理平台', template_mode='bootstrap3')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    admin.init_app(app)

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/weapp')

    # 配置flask-admin模型视图
    from .models import Answer, Question, Book, Comment, CSessionInfo
    admin.add_view(ModelView(Answer, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Book, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(CSessionInfo, db.session))

    return app
