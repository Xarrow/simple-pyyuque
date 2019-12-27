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

import os

import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)

IS_DEBUG = logger.level == logging.DEBUG

YUQUE_OAUTH_AUTHORIZE_URL = "https://www.yuque.com/oauth2/authorize"
YUQUE_OAUTH_EXCHANGE_TOKEN_URL = 'https://www.yuque.com/oauth2/token'
YUQUE_BASIC_V2_API_URL = 'https://www.yuque.com/api/v2/'

MESSAGE_TEMPLATE_A = """# {method_name} , `{p1}` and `{p2}` can not both be blank ! For further API detail please visit `{doc_uri}` """
MESSAGE_TEMPLATE_B = """# {method_name} , `{p1}` is not blank ! For further API detail please visit `{doc_uri}` """


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


class YuQueAPIException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class YuQueAPIUnauthorized(Exception):
    def __init__(self, message) -> None:
        self.message = message


class PersistentCallbackBaseException(Exception):
    def __init__(self, message) -> None:
        self.message = message


import platform

WINDOWS = 'windows' in platform.platform()
LINUX = sys.platform.startswith('linux')
DARWIN = sys.platform.startswith('darwin')

DEBIAN = 'debian' in platform.platform()
CENTOS = 'centos' in platform.platform()
