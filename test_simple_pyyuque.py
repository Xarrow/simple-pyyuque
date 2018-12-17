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
from simple_pyyuque import *

lark_api = SimplePyYuQueAPI(token="token", app_name="py_yuque1")
user_api = lark_api.User()
group_api = lark_api.Group()
repo_api = lark_api.Repo()
doc_api = lark_api.Doc()


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

    def test_get_users_repos(self):
        res = repo_api.get_users_repos(type="all", login="Helixcs").base_response
        print(res)

    def test_post_users_repos(self):
        res = repo_api.post_users_repos(name="Helixcs 的仓库123",
                                        slug="helixcs123",
                                        description="Helixcs 的仓库123",
                                        public=RepoPublic.ALL_OPEN,
                                        type=RepoType.BOOK,
                                        login="Helixcs",
                                        )

        res = repo_api.create_repos(name="Helixcs 的仓库123",
                                    slug="helixcs123",
                                    description="Helixcs 的仓库123",
                                    public=RepoPublic.ALL_OPEN,
                                    type=RepoType.BOOK,
                                    login="Helixcs",
                                    )

        print(res)
        # https://www.yuque.com/helixcs/helixcs123

    def test_get_repos(self):
        # res = repo_api.get_repos_detail(namespace="helixcs/helixcs123")
        # res = repo_api.get_repos(namespace="helixcs/helixcs123")
        # res = repo_api.get_repos_detail(id=189411)
        res = repo_api.get_repos(id=189411)
        print(res.base_response)

    def test_put_repos(self):
        toc = '''
        - [New Node1]()
        - [new Doc1-1](avm3rn "1056206")
        - [new Doc2-1](xvmadh)
        - [new Doc1-2](uhdxg5)
        - [new Doc2](lb3i5k)
        - [New Doc3](oi5u6l "1056203")
'''
        res = repo_api.put_repos(name="helixcs234 仓库",
                                 slug="helixcs234",
                                 toc="",
                                 description="Helixcs 仓库234",
                                 public=RepoPublic.PRIVATE,
                                 namespace="helixcs/helixcs123").base_response

        res = repo_api.update_repos(name="helixcs234 仓库",
                                    slug="helixcs234",
                                    toc="",
                                    description="Helixcs 仓库234",
                                    public=RepoPublic.PRIVATE,
                                    namespace="helixcs/helixcs123").base_response

        print(res)
        # https://www.yuque.com/helixcs/helixcs234

    def test_delete_repos(self):
        res = repo_api.delete_repo(namespace="helixcs/helixcs234")
        res = repo_api.delete_repo(id=189411)

    def test_repos_toc(self):
        res = repo_api.repos_toc(namespace="helixcs/helixcs234")
        res = repo_api.repos_toc(id=189411).base_response
        print(res)

    def test_search_repos(self):
        res = repo_api.search_repos(q='a', type=RepoType.BOOK).base_response
        print(res)

    def test_get_repos_docs(self):
        res = doc_api.get_repos_docs(namespace="helixcs/helixcs234").base_response
        res = doc_api.get_repos_docs(id=189411).base_response
        print(res)

    def test_get_repos_docs_detail(self):
        res = doc_api.get_repos_docs_detail(namespace="helixcs/tuyepi", slug="taosm3").base_response
        res = doc_api.get_docs_detail(namespace="helixcs/tuyepi", slug="taosm3").base_response
        print(res)

    def test_create_docs(self):
        res = doc_api.post_repos_docs(namespace="helixcs/helixcs234", slug="randomstring", title="测试",
                                      body="你好世界!").base_response
        res = doc_api.create_docs(namespace="helixcs/helixcs234", slug="randomstring", title="测试",
                                  body="你好世界!").base_response

        # https://www.yuque.com/helixcs/helixcs234/randomstring

    def test_update_docs(self):
        res = doc_api.put_repos_docs(namespace="helixcs/helixcs234", id=1057879, title="测试更新", slug="randomstring",
                                     public=DocPublic.OPEN,
                                     body="你好世界! (修改body)").base_response
        res = doc_api.update_docs(namespace="helixcs/helixcs234", id=1057879, title="测试更新", slug="randomstring",
                                  public=DocPublic.OPEN,
                                  body="你好世界! (修改body)").base_response

        res = doc_api.put_repos_docs(repo_id=189411, id=1057879, title="测试更新", slug="randomstring",
                                     public=DocPublic.OPEN,
                                     body="你好世界! (修改body)").base_response

        res = doc_api.update_docs(repo_id=189411, id=1057879, title="测试更新", slug="randomstring",
                                  public=DocPublic.OPEN,
                                  body="你好世界! (修改body)").base_response
        print(res)
        # https://www.yuque.com/helixcs/helixcs234/randomstring

    def test_delete_docs(self):
        res = doc_api.delete_repos_docs(namespace="helixcs/helixcs234", id=1057879).base_response
        res = doc_api.delete_repos_docs(repo_id=189411, id=1057879).base_response

        res = doc_api.delete_docs(namespace="helixcs/helixcs234", id=1057879).base_response
        res = doc_api.delete_docs(repo_id=189411, id=1057879).base_response

        print(res)


if __name__ == '__main__':
    try:
        t = TestPyYuQue()
        # t.test_get_groups()
        # t.test_get_groups_detail()
        # t.test_update_groups()
        # t.test_get_groups_users()
        # t.test_put_groups_users()
        t.test_get_users_repos()
        # t.test_post_users_repos()
        # t.test_get_repos()
        # t.test_put_repos()
        t.test_repos_toc()
        t.test_search_repos()
        t.test_get_repos_docs()
        t.test_get_repos_docs_detail()
        # t.test_create_docs()
        t.test_update_docs()
    except Exception as ex:
        pass
