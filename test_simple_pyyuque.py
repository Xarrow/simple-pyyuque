# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: test_yuque
 Time: 2018/12/12
 
 Add New Functional TestPyYuQue
"""
import unittest
from .simple_pyyuque import SimplePyYuQueAPI

lark_api = SimplePyYuQueAPI(token="LIpEyM947oR2ZjmEdgCd6ByKPQUlLd39UrrtXVlS", app_name="py_yuque1")
user_api = lark_api.User()


class TestPyYuQue(unittest.TestCase):

    def test_get_user(self):
        assert user_api.get_user() is not None
        assert user_api.user is not None

    def test_get_users(self):
        assert user_api.get_users(login="Helixcs") is not None


if __name__ == '__main__':
    unittest.main()
