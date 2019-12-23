# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_oauth.py
 Time: 2019/12/23
"""
import base64
import hashlib
import hmac
import pickle
import time
import webbrowser
import os
import requests

from typing import Union
from urllib.parse import urlencode

from simple_pyyuque_utils import generate_random_code, YUQUE_OAUTH_EXCHANGE_TOKEN_URL, YUQUE_BASIC_V2_API_URL, \
    YUQUE_OAUTH_AUTHORIZE_URL


class PersistentCallbackBase(object):
    def __init__(self, persistent_path: str, token_map: dict = None):
        self._persistent_path = persistent_path
        self._local_persistent_path = None
        self._token_map = token_map

    def do_persistent(self):
        raise Exception("not implement")

    def do_fetch(self):
        raise Exception("not implement")

    @property
    def local_persistent_path(self):
        return self._local_persistent_path

    @property
    def token_map(self):
        return self._token_map


class JsonPersistentCallback(PersistentCallbackBase):
    def do_persistent(self):
        pass

    def do_fetch(self):
        pass


class PicklePersistentCallback(PersistentCallbackBase):
    def do_persistent(self):
        if self._token_map.get('access_token') is None:
            return self
        is_file = True
        # dir
        if self._persistent_path.endswith("/") or os.path.isdir(self._persistent_path):
            is_file = False
            if not os.path.isdir(self._persistent_path):
                os.makedirs(self._persistent_path)
        # file
        else:
            dir_path = os.path.dirname(self._persistent_path)
            if not os.path.isdir(os.path.abspath(dir_path)):
                os.makedirs(dir_path)

        tmp = self._persistent_path
        if not is_file:
            tmp = os.path.join(self._persistent_path, "token.pickle")
        with open(tmp, mode='wb') as fd:
            pickle.dump(self._token_map, fd)

        self._local_persistent_path = tmp
        return self

    def do_fetch(self):
        if self._local_persistent_path is None:
            if os.path.isdir(self._persistent_path):
                ll = os.listdir(self._persistent_path)
                if len(ll) > 0:
                    for i in ll:
                        if i.endswith("pickle"):
                            tmp = os.path.join(self._persistent_path, i)
            elif os.path.isfile(self._persistent_path):
                tmp = self._persistent_path
            else:
                raise Exception("")
        else:
            tmp = self._local_persistent_path

        with open(tmp, mode="rb") as fd:
            _tmp_token_map = pickle.load(fd, encoding='utf-8')
            self._token_map = _tmp_token_map
        return self


class SimpleYuQueOAuth4Web(object):
    pass


class SimpleYuQueOAuth4Server(object):
    # https://www.yuque.com/yuque/developer/authorizing-oauth-apps#Z8ye5
    def __init__(self,
                 client_id: Union[str, bytes] = None,
                 secret_id: Union[str, bytes] = None,
                 scope: str = "doc,repo,group:read",
                 open_in_console: bool = True,
                 persistent_path: str = os.path.curdir,
                 persistent_callback=PicklePersistentCallback):

        self._client_id = client_id
        self._secret_id = secret_id
        self._scope = scope
        self._open_in_console = open_in_console
        self._auth_map = {"client_id": self._client_id if isinstance(self._client_id, str) else str(self._client_id,
                                                                                                    encoding='utf-8'),
                          "code": generate_random_code(),
                          "response_type": "code",
                          "scope": self._scope,
                          "timestamp": str(int(time.time() * 1000))}
        self._auth_url = ""
        self._auth_code = ""
        self._token_map = None
        self._persistent_path = persistent_path
        self._persistent_callback = persistent_callback
        self._persistent_callback_instance = self._persistent_callback(persistent_path=self._persistent_path,
                                                                       token_map=self._token_map)

    def _sign(self):
        message = bytes(urlencode(query=self._auth_map, encoding='utf-8'), encoding='utf-8')
        dig = hmac.new(
            key=self._secret_id if isinstance(self._secret_id, bytes) else bytes(self._secret_id, encoding='utf-8'),
            msg=message,
            digestmod=hashlib.sha1).digest()
        sign = base64.b64encode(dig).decode()
        self._auth_map['sign'] = sign
        return self

    def _auth_urlencode(self):
        self._auth_url = '{0}?{1}'.format(YUQUE_OAUTH_AUTHORIZE_URL, urlencode(self._auth_map))
        return self

    def _wait_for_auth_code(self):
        if self._open_in_console:
            print("Please copy url {0} in browser and paste code in shell.".format(self._auth_url))
        else:
            try:
                webbrowser.open(url=self._auth_url)
            except Exception as ex:
                print("Your Platform can not support webbrowser.")
                raise ex
        self._auth_code = input("Please enter your code:")
        return self

    def _exchange_token(self):
        exchange_data = {
            "client_id": self._client_id if isinstance(self._client_id, str) else str(self._client_id,
                                                                                      encoding='utf-8'),
            "code": self._auth_code,
            "grant_type": "client_code"
        }
        res = requests.post(url=YUQUE_OAUTH_EXCHANGE_TOKEN_URL, data=exchange_data)
        self._token_map = res.json()
        return self

    def _persistent_token(self):
        self._persistent_callback_instance.do_persistent()
        return self

    def _fetch_token(self):
        if self._token_map is None:
            self._token_map = self._persistent_callback_instance.do_fetch().token_map
        return self

    def upload_attach(self, local_file_path: str = None, description: str = None):
        upload_attach_api = "{0}/{1}".format(YUQUE_BASIC_V2_API_URL, "upload/attach")
        _headers = {
            'User-agent': 'yuqueapp',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Auth-Token': self._token_map.get("access_token")
        }
        res = requests.post(url=upload_attach_api, files={"file": open(r'/Users/helix/Desktop/24.jpg')})
        print(res.text)
        pass

    @property
    def token_map(self):
        return self._token_map

    def run(self):
        self._sign()
        self._auth_urlencode()
        self._wait_for_auth_code()
        self._exchange_token()
        self._persistent_token()

        return self


if __name__ == '__main__':
    a = SimpleYuQueOAuth4Server(client_id="TSJjgMa1QIj5acgAHcvF",
                                secret_id="jr700ZxttSJeZmJllJFC3qGn659zRLMeUOSlWdJF",
                                open_in_console=True,
                                persistent_path="aaa.pickle")
    print(a.run().upload_attach())

    pass
