from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from config import config

db = SQLAlchemy()
admin = Admin(name='在线测试小程序管理平台', template_mode='bootstrap3')
babel = Babel()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

    config[config_name].init_app(app)

    db.init_app(app)
    admin.init_app(app)
    babel.init_app(app)

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/weapp')

    # 配置flask-admin模型视图
    from .models import Answer, Question, Exam, CSessionInfo
    admin.add_view(AnswerModelView(Answer, db.session, name='答案统计'))
    admin.add_view(QuestionModelView(Question, db.session, name='试题管理'))
    admin.add_view(ExamModelView(Exam, db.session, name='试卷管理'))
    admin.add_view(ModelView(CSessionInfo, db.session, name='用户管理'))

    return app


class ExamModelView(ModelView):
    column_labels = {
        'gid': '试卷编号',
        'gname': '试卷名称',
        'lname': '课程名称',
        'total': '总分',
        'start_time': '考试开始时间',
        'end_time': '考试结束时间'
    }


class QuestionModelView(ModelView):
    column_labels = {
        'gid': '试卷编号',
        'gname': '试卷名称',
        'num': '题号',
        'type': '题型',
        'content': '题目内容',
        'answer': '标准答案',
        'score': '试题分数',
        'result_a': '选项A',
        'result_b': '选项B',
        'result_c': '选项C',
        'result_d': '选项D'
    }


class AnswerModelView(ModelView):
    column_labels = {
        'openid': '用户编号',
        'gid': '试卷编号',
        'gname': '试卷名称',
        'answers': '用户答案',
        'total': '得分',
        'submit_time': '提交时间'
    }
