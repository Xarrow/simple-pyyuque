# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: __init__.py
 Time: 2018/12/9
 
 Add New Functional __init__.py
"""
import sys

try:
    assert sys.version_info.major >= 3
except Exception as ex:
    raise AssertionError("simple-pyyuque only support 3+ !")

from .simple_pyyuque import *
from .simple_pyyuque_typing import *
