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
from simple_pyyuque import SimplePyYuQueAPI

lark_api = SimplePyYuQueAPI(token="LIpEyM947oR2ZjmEdgCd6ByKPQUlLd39UrrtXVlS", app_name="py_yuque1")
user_api = lark_api.User()
group_api = lark_api.Group()


class TestPyYuQue(object):

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
        assert group_api.get_public_groups() is not None
        assert group_api.public_groups is not None

    def test_post_groups(self):
        res = group_api.post_group(name="Helixcs 的组织名称", login="Helixcs123",
                                   description="Helixcs 的组织描述")
        print(res)

    def test_get_groups_detail(self):
        res1 = group_api.get_groups_detail(id=225250).base_response
        print(res1)
        res2 = group_api.get_groups_detail(login="Helixcs123").base_response
        print(res2)

    def test_update_groups(self):
        # res = group_api.put_groups(login="Helixcs123",name="Helixcs 的组织名称更新1次",login_update="Helixcs456",description="Helixcs123 更新为Helixcs456")
        res = group_api.update_groups(login="Helixcs456", name="Helixcs 的组织名称更新2次", login_update="Helixcs789",
                                      description="Helixcs456 更新为Helixcs789")
        print(res)

    def test_delete_groups(self):
        res = group_api.delete_groups(login="Helixcs456")
        res = group_api.delete_groups(id=225250)
        print(res)
        pass

    def test_get_groups_users(self):
        res = group_api.get_groups_users(login="Helixcs456").base_response
        res = group_api.get_groups_users(id=225250).base_response
        print(res)
        pass

    def test_put_groups_users(self):
        res = group_api.put_groups_users(group_login="Helixcs456",
                                         login="Helixcs",
                                         role=1)
        res = group_api.update_group_users(group_login="Helixcs456",
                                           login="Helixcs",
                                           role=1)
        print(res)

    def test_delete_groups_users(self):
        res = group_api.delete_groups_users(group_login="Helixcs456",
                                            login="OtherUser")

        res = group_api.delete_groups_users(group_id=225250,
                                            login="OtherUser")

        print(res)


if __name__ == '__main__':
    t = TestPyYuQue()
    # t.test_get_groups()
    # t.test_get_groups_detail()
    # t.test_update_groups()
    # t.test_get_groups_users()
    # t.test_put_groups_users()
