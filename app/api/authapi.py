import time
import sys
import random
import urllib.parse
import hashlib
import base64
import json

import requests

from .utils import ksort, hash_hmac, storeUserInfo, decrypt
from .consts import Auth
from .config import WxConfig
from ..models import CSessionInfo


class AuthAPI():

    @staticmethod
    def auth(code, encryptedData, iv):
        result = AuthAPI.get_sessionkey(code)
        session_key = result['session_key']
        openid = result['openid']
        skey = hashlib.sha1((session_key + str(random.randint(0, sys.maxsize))).encode()).hexdigest()

        if code and not encryptedData and not iv:
            userInfo = CSessionInfo.query.filter_by(
                open_id=openid).first()
            wxUserInfo = json.loads(userInfo.user_info)

            # 更新登录态
            storeUserInfo(wxUserInfo, skey, session_key)

            return {
                'login_state': Auth.SUCC,
                'userinfo': {
                    'userinfo': wxUserInfo,
                    'skey': skey
                }
            }

        userInfo = decrypt(session_key, encryptedData, iv)
        storeUserInfo(userInfo, skey, session_key)

        return {
            'login_state': Auth.SUCC,
            'userinfo': {
                'userinfo': userInfo,
                'skey': skey
            }
        }

    @staticmethod
    def get_sessionkey(code):
        useQcProxy = WxConfig.useQcloudLogin

        # 是否使用腾讯云代理登录
        # useQcProxy 为 true
        # sdk 将会使用腾讯云的 QcloudSecretId 和 QcloudSecretKey 获取 session key
        # 反之将会使用小程序的 AppID 和 AppSecret 获取 session key
        if (useQcProxy):
            secretId = WxConfig.qcloudSecretId
            secretKey = WxConfig.qcloudSecretKey
            return AuthAPI.useQcloudProxyGetSessionKey(secretId, secretKey, code)
        else:
            appId = WxConfig.appId
            appSecret = WxConfig.appSecret
            return AuthAPI.getSessionKeyDirectly(appId, appSecret, code)

    @staticmethod
    def getSessionKeyDirectly(appId, appSecret, code):
        requestParams = {
            'appid': appId,
            'secret': appSecret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        url = 'https://api.weixin.qq.com/sns/jscode2session?' + urllib.parse.urlencode(requestParams)
        r = requests.get(url, timeout=WxConfig.networkTimeout)
        status = r.status_code
        body = r.json()

        if status != 200 or body is None or 'errcode' in body:
            raise Exception('直接获取sessionkey失败: ' + json.dumps(body))
        return body

    @staticmethod
    def useQcloudProxyGetSessionKey(secretId, secretKey, code):
        if (secretId is None) or (secretKey is None) or (code is None):
            raise Exception('腾讯云代理参数为空')

        requestUrl = 'wss.api.qcloud.com/v2/index.php'
        requestMethod = 'GET'
        requestData = {
            'Action': 'GetSessionKey',
            'js.code': code,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, sys.maxsize),
            'SecretId': secretId,
            'SignatureMethod': 'HmacSHA256'
        }

        requestData = ksort(requestData)
        requestString = urllib.parse.urlencode(requestData)
        signatureRawString = requestMethod + requestUrl + '?' + requestString

        sign = base64.b64encode(
            hash_hmac(hashlib.sha256, signatureRawString, secretKey))
        requestData['Signature'] = bytes.decode(sign)

        url = 'https://' + requestUrl + '?' + urllib.parse.urlencode(requestData)
        r = requests.get(url, timeout=WxConfig.networkTimeout)
        status = r.status_code
        body = r.json()

        if status != 200 or body is None or body['code'] != 0:
            raise Exception('腾讯云代理登录失败')

        if 'errcode' in body['data']:
            raise Exception('腾讯云代理登录失败' + ': ' + json.dumps(body['data']))

        return body['data']
