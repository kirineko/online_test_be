from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from config import config

import flask_login as login

db = SQLAlchemy()
babel = Babel()
app = Flask(__name__)

from .models import Answer, Question, Exam, CSessionInfo, User
from .modelview import MyAdminIndexView
admin = Admin(name='在线测试小程序管理平台', index_view=MyAdminIndexView(),
              base_template='my_master.html')

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


def create_app(config_name):
    app.config.from_object(config[config_name])
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

    config[config_name].init_app(app)

    db.init_app(app)
    admin.init_app(app)
    babel.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    init_login()

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/weapp')

    # 配置flask-admin模型视图
    from .modelview import AnswerModelView, QuestionModelView
    from .modelview import ExamModelView, UserModelView, WechatModelView
    admin.add_view(AnswerModelView(Answer, db.session, name='答案统计'))
    admin.add_view(QuestionModelView(Question, db.session, name='试题管理'))
    admin.add_view(ExamModelView(Exam, db.session, name='试卷管理'))
    admin.add_view(WechatModelView(CSessionInfo, db.session, name='微信用户查看'))
    admin.add_view(UserModelView(User, db.session, name='用户管理'))

    return app
