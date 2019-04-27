from flask import jsonify, request
from . import api
from .consts import Auth
from .authapi import AuthAPI


@api.route('/login')
def login():
    result = _login()
    if result['login_state'] == Auth.SUCC:
        response = jsonify({
            'code': 0,
            'data': result['userinfo']
        })
    else:
        response = jsonify({
            'code': -1,
            'error': result['error']
        })
    return response


def _login():
    header = request.headers
    try:
        code = header.get('X-Wx-Code')
        encryptedData = header.get('X-Wx-Encrypted-Data')
        iv = header.get('X-Wx-Iv')

        if not code:
            raise Exception('请求头未包含 code，请配合客户端 SDK 登录后再进行请求')
        return AuthAPI.auth(code, encryptedData, iv)
    except Exception as err:
        result = {
            'login_state': Auth.FAIL,
            'error': err.args[0]
        }
        return result
