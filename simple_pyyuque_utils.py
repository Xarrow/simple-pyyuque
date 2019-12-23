# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_util.py
 Time: 2019/12/19
"""
import logging
import random
from typing import Optional, Union
from urllib.parse import urlencode

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)

IS_DEBUG = logger.level == logging.DEBUG


def is_blank(value: Optional[Union[int, str, dict, list, bytes, tuple]]) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return True if value is None or value.strip('') == '' else False
    if isinstance(value, dict):
        return True if len(value) < 1 else False
    if isinstance(value, list):
        return True if len(value) < 1 else False
    if isinstance(value, bytes):
        return True if value == b'' else False
    # (None,None) ==> False
    if isinstance(value, tuple):
        if len(value) < 1:
            return True
        for i in value:
            if i is not None:
                return False
        return True
    if isinstance(value, set):
        return True if len(value) < 1 else False
    return False


def is_not_blank(value: Optional[Union[int, str, dict, list, tuple,]]) -> bool:
    return not is_blank(value=value)


def generate_random_string_with_digest(length: int = 6) -> str:
    _seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _sa = []
    for i in range(length):
        _sa.append(random.choice(_seed))
    _rds = "".join(_sa)
    return _rds


def generate_slug() -> str:
    return generate_random_string_with_digest()


def generate_random_code() -> str:
    return generate_random_string_with_digest(40)


import hashlib
import hmac
import time
import base64
import requests


# https://www.yuque.com/oauth2/authorize?client_id=TSJjgMa1QIj5acgAHcvF&scope=doc,repo,group:read&redirect_uri=http://localhost:7777/yuqueCallback&state=2&response_type=code
def sign(query: dict, secret: str) -> str:
    urlencode_string = urlencode(query=query, encoding='utf-8')
    print(urlencode_string)
    dig = hmac.new(key=b"jr700ZxttSJeZmJllJFC3qGn659zRLMeUOSlWdJF",
                   msg=bytes(urlencode_string, encoding='utf-8'),
                   digestmod=hashlib.sha1).digest()
    return base64.b64encode(dig).decode()


if __name__ == '__main__':
    random_code = generate_random_code()
    query_map = {"client_id": "TSJjgMa1QIj5acgAHcvF", "code": random_code, "response_type": "code",
                 "scope": "doc,repo,group:read", "timestamp": str(int(time.time() * 1000))}
    sign = (sign(query=query_map, secret="jr700ZxttSJeZmJllJFC3qGn659zRLMeUOSlWdJF"))
    query_map['sign'] = sign
    print(query_map)
    print('https://www.yuque.com/oauth2/authorize?'+urlencode(query_map))
    res = requests.get(url='https://www.yuque.com/oauth2/authorize', params=query_map, )
    print(res.text)
