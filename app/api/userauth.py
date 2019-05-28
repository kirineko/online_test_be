from flask import request
from . import api
from .utils import jsonsucc, jsonerr
from .. import db
from ..models import User


@api.route('/auth', methods=['post'])
def userauth():
    args = request.get_json()
    openid = args.get('openid')
    usernumber = args.get('usernumber')
    password = args.get('password')

    user = User.query.filter_by(usernumber=usernumber).first()
    if user is None:
        return jsonerr(-1, '用户不存在')
    if user.openid and user.openid != openid:
        return jsonerr(-1, '该用户已经绑定其它微信账号，请退出再操作')
    if user.password == password:
        user.openid = openid
        db.session.add(user)
        db.session.commit()
        login_user = {
            'username': user.username
        }
        return jsonsucc(login_user)
    else:
        return jsonerr(-1, '密码错误')


@api.route('/unbind', methods=['post'])
def unbind():
    args = request.get_json()
    openid = args.get('openid')

    user = User.query.filter_by(openid=openid).first()
    if user is None:
        return jsonerr(-1, '用户不存在')

    user.openid = ''
    db.session.add(user)
    db.session.commit()
    result = {
        'msg': '解绑成功'
    }
    return jsonsucc(result)
