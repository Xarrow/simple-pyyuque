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
from simple_pyyuque import SimplePyYuQueAPI

lark_api = SimplePyYuQueAPI(token="LIpEyM947oR2ZjmEdgCd6ByKPQUlLd39UrrtXVlS", app_name="py_yuque1")
user_api = lark_api.User()
group_api = lark_api.Group()


class TestPyYuQue(unittest.TestCase):

    def test_get_user(self):
        assert user_api.get_user() is not None
        assert user_api.user is not None

    def test_get_users(self):
        assert user_api.get_users(login="Helixcs") is not None

    def test_get_user_docs(self):
        assert user_api.get_user_docs(q='', offset=1) is not None

    def test_get_user_recent_updated(self):
        assert user_api.get_user_recent_updated() is not None

    def test_get_users_groups(self):
        assert group_api.get_users_groups(login="Helixcs") is not None

    def test_get_groups(self):
        assert group_api.get_public_groups() is not  None
        assert group_api.public_groups is not  None
if __name__ == '__main__':
    unittest.main()
