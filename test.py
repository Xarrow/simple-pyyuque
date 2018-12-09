# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: test
 Time: 2018/12/9
 
 Add New Functional test
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False

if sys.version > '3':
    PY3 = True

from simple_pyyuque import SimplePyYuQueAPI

if __name__ == '__main__':
    y = SimplePyYuQueAPI(token="Token", app_name="py_yuque1")
    # Repo
    print(y.get_users_repos(login="Helixcs").base_response)
    # print(y.create_users_repos(login="Helixcs", name="daddadsaadsad", slug="").base_response)
    # print(y.get_repos(namespace="rn15gw/ig2r81").base_response)
    # print(y.put_repos(namespace="rn15gw/ig2r81", name="11111", slug='ig2r81', toc='ipchkk').base_response)
    # print(y.delete_repo(namespace="rn15gw/ig2r81"))
    print(y.repos_toc(namespace="helixcs/tuyepi").base_response)
    print(y.search_repos(q="doc").base_response)
    # Docs
    print(y.get_repos_docs(namespace="helixcs/tuyepi").base_response)
    print(y.get_repos_docs_detail(namespace="helixcs/tuyepi", slug="taosm3").base_response)
    print(y.post_repos_docs(namespace="rn15gw/dyrs3g", slug="taosm31", title="测试", body="你好世界!").base_response)
    print(y.put_repos_docs(namespace="rn15gw/dyrs3g", id=1040079, slug="taosm31", title="测试",
                           body="你好世界! update").base_response)
    print(y.delete_repos_docs(namespace="rn15gw/dyrs3g", id=1040082).base_response)
