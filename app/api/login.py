from flask import request
from . import api
from .consts import Auth
from .authapi import AuthAPI
from .utils import jsonerr, jsonsucc


@api.route('/login')
def login():
    result = _login()
    if result['login_state'] == Auth.SUCC:
        response = jsonsucc(result['userinfo'])
    else:
        response = jsonerr(-1, result['error'])
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
