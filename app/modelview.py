from flask_admin.contrib.sqla import ModelView
import flask_login as login
import flask_admin as admin
from flask import url_for, redirect, request
from wtforms import form, fields, validators
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    usernumber = fields.StringField(label='工号', validators=[validators.required()])
    password = fields.PasswordField(label='密码', validators=[validators.required()])
    role = fields.SelectField(
        label='角色', choices=[(1, '教师'), (2, '管理员')], coerce=int)

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(usernumber=self.usernumber.data).first()


class RegistrationForm(form.Form):
    usernumber = fields.StringField(label='工号', validators=[validators.required()])
    username = fields.StringField(label='用户名', validators=[validators.required()])
    password = fields.PasswordField(label='密码', validators=[validators.required()])
    role = fields.SelectField(
        label='角色', choices=[(1, '教师'), (2, '管理员')], coerce=int)

    def validate_login(self, field):
        if db.session.query(User).filter_by(usernumber=self.usernumber.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>没有账号? <a href="' + url_for('.register_view') + '">点击注册</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>已有账号? <a href="' + \
            url_for('.login_view') + '">点击登录</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ExamModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.role == 1

    column_labels = {
        'gid': '试卷编号',
        'gname': '试卷名称',
        'lname': '课程名称',
        'total': '总分',
        'start_time': '考试开始时间',
        'end_time': '考试结束时间'
    }


class QuestionModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.role == 1

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

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.role == 1

    column_labels = {
        'openid': '用户编号',
        'gid': '试卷编号',
        'gname': '试卷名称',
        'answers': '用户答案',
        'total': '得分',
        'submit_time': '提交时间'
    }


class UserModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.role == 2

    column_labels = {
        'usernumber': '学号/工号',
        'username': '姓名',
        'password': '密码',
        'role': '用户角色',
        'dept': '院系',
        'openid': 'openid'
    }

    form_overrides = {
        'role': fields.SelectField
    }

    form_args = {
        'role': {
            'choices': {
                (1, '教师'),
                (2, '管理员')
            },
            'coerce': int
        }
    }
    form_excluded_columns = ['openid']
    column_exclude_list = ['openid']


class WechatModelView(ModelView):

    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.role == 2

    column_labels = {
        'open_id': 'openid',
        'uuid': 'uuid',
        'skey': 'skey',
        'create_time': '创建时间',
        'last_visit_time': '最后登录时间',
        'session_key': 'sessionkey',
        'user_info': '用户信息'
    }
