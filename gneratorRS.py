# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: gneratorRS
 Time: 2018/12/13
 
 Add New Functional gneratorRS
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False

from simple_pyyuque import SimplePyYuQueAPI,UserDescriptionType

user = SimplePyYuQueAPI(token="LIpEyM947oR2ZjmEdgCd6ByKPQUlLd39UrrtXVlS", app_name="py_yuque1").User()
# User
user_base = user.get_user_recent_updated(type=UserDescriptionType.BOOK)

ss = '''
|属性|类型|示例|说明|
|---|-----|----|----|

'''

for k, v in user_base.base_response[0].items():
    if isinstance(v, str):
        _res = "string"
    elif isinstance(v, int):
        _res = "int"
    elif isinstance(v, dict):
        _res = "dict"
        v = "dict"
    elif isinstance(v, list):
        _res = "list"
        v = "list"
    else:
        _res = "None"

    sinle_property = """|{0}|{1}|{2}|{3}|\n""".format(k, _res, v, "")
    ss = ss + sinle_property

print(ss)
