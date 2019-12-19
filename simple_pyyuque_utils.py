# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_util.py
 Time: 2019/12/19
"""
import random
from typing import Optional, Union
import logging

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
logger.setLevel(level)

IS_DEBUG = logger.level == logging.DEBUG


def is_blank(value: Optional[Union[int, str, dict, list]]) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return True if value is None or value.strip('') == '' else False
    if isinstance(value, dict):
        return True if len(value) < 1 else False
    if isinstance(value, list):
        return True if len(value) < 1 else False
    return False


def is_not_blank(value: Optional[Union[int, str, dict, list]]) -> bool:
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
