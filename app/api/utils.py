import hmac
import binascii
import os
import time
import json
import base64
from Crypto.Cipher import AES

from ..models import CSessionInfo
from .. import db


def ksort(d):
    return {k: d[k] for k in sorted(d.keys())}


def hash_hmac(algo, data, key):
    res = hmac.new(key.encode(), data.encode(), algo).digest()
    return res


def storeUserInfo(userinfo, skey, session_key):
    uuid = bytes.decode(binascii.hexlify(os.urandom(16)))
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    last_visit_time = create_time
    open_id = userinfo['openId']
    user_info = json.dumps(userinfo)

    res = CSessionInfo.query.filter_by(
        open_id=open_id).first()

    if res is None:
        kargs = {
            'uuid': uuid,
            'skey': skey,
            'create_time': create_time,
            'last_visit_time': last_visit_time,
            'open_id': open_id,
            'session_key': session_key,
            'user_info': user_info
        }
        csessioninfo = CSessionInfo(**kargs)
        db.session.add(csessioninfo)
        db.session.commit()
    else:
        res.skey = skey
        res.last_visit_time = last_visit_time
        res.session_key = session_key
        res.user_info = user_info
        db.session.add(res)
        db.session.commit()


def decrypt(sessionKey, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(_unpad(cipher.decrypt(encryptedData)))

        return decrypted


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]
