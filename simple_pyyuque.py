# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque
 Time: 2018/12/9
 
 Add New Functional simple_pyyuque
"""

import asyncio

import requests

from simple_pyyuque_typing import *
from simple_pyyuque_utils import *


class BaseAPI(object):
    __slots__ = ['_session', '_loop', '_token', '_app_name', '_headers']

    def __init__(self, token: str, app_name: str, **kwargs):
        assert is_not_blank(value=token)
        self._token = token
        self._app_name = app_name
        self._session = requests.Session()
        self._loop = asyncio.get_event_loop()
        self._headers = {
            'User-agent': self._app_name,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Auth-Token': self._token

            # PI//ucsAYu0rogOlbMvL9jsVqRbkenxCVxlkiSFRNAngUMUmyAxktqR8Fi/2Z5FQbfGYNPM7OW171HjWKnRdZYRHJm+r8RGkC465uuXTrCCh06Fb22VkoDl0CidDd9nBYcxMvD70YPBRk+7p8CUhKWT+3OR5dmuHMJF+zeB1WQU=
        }

    def _api_request(self, method: object, source_name: str, **kwargs) -> Optional[dict]:
        if isinstance(method, str):
            kwargs['method'] = method
        elif isinstance(method, RequestMethods):
            kwargs['method'] = method.value

        kwargs['url'] = \
            YUQUE_BASIC_V2_API_URL + (
                source_name if not source_name.startswith("/") else source_name[1:len(source_name)])
        kwargs['headers'] = self._headers

        if IS_DEBUG:
            logger.debug("#_api_request , requests kwargs=%s" % kwargs)

        async def _inner_request():
            async def _a():
                return self._session.request(**kwargs)

            return await _a()

        res = self._loop.run_until_complete(_inner_request())
        sc = res.status_code
        if sc != 200:
            message = "#_api_request , request failed , request kwargs=%s , messages=%s - %s  , result=%s  ,response headers=%s" % (
                kwargs, sc, STATUS_CODE_MAPPING.get(sc), res.text, res.headers)
            logger.error(message)
            raise YuQueAPIException(message)
        # 探测正确返回
        try:
            res.json()
        except Exception as ex:
            message = "#_api_request , response is not json type , request kwargs=%s , messages=%s - %s  , result=%s  ,response headers=%s" % (
                kwargs, sc, STATUS_CODE_MAPPING.get(sc), res.text, res.headers)
            logger.error(message)
            raise YuQueAPIException(message)
        return res.json().get("data") if is_not_blank(res.json().get('data')) else None

    def get_request(self, source_name: str, res_type, **kwargs) -> Optional[Union[dict, BaseSerializer]]:
        res = self._api_request(method=RequestMethods.GET, source_name=source_name, **kwargs)
        if res_type is not None:
            return res_type(res)
        return res

    def post_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.POST, source_name=source_name, **kwargs)
        if res_type is not None:
            return res_type(res)
        return res

    def put_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.PUT, source_name=source_name, **kwargs)
        if res_type is not None:
            return res_type(res)
        return res

    def delete_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.DELETE, source_name=source_name, **kwargs)
        if res_type is not None:
            return res_type(res)
        return res

    def head_request(self, source_name: str, res_type, **kwargs) -> Optional[dict]:
        res = self._api_request(method=RequestMethods.HEAD, source_name=source_name, **kwargs)
        if res_type is not None:
            return res_type(res)
        return res


# like as global instance
class BaseRelation(object):
    def __init__(self):
        self._yuque_api = None

    @property
    def yuque_api(self) -> BaseAPI:
        return self._yuque_api

    @yuque_api.setter
    def yuque_api(self, value: BaseAPI):
        self._yuque_api = value


class SimplePyYuQueAPI(BaseAPI):

    def __init__(self, token: str, app_name: str, **kwargs):
        super().__init__(token, app_name, **kwargs)
        BaseRelation.yuque_api = self

    # User - 用户
    # @See https://www.yuque.com/yuque/developer/user
    class User(BaseRelation):
        def get_user(self) -> Optional[UserSerializer]:
            """
            获取认证的用户的个人信息,获取当前 Token 对应的用户的个人信息。

            :return:
            """
            return self.yuque_api.get_request(source_name="user", res_type=UserSerializer)

        @property
        def user(self) -> Optional[UserSerializer]:
            return self.get_user()

        def get_users(self, id: int = None, login: str = None) -> Optional[UserSerializer]:
            """
            获取单个用户信息,基于用户 login 或 id 获取一个用户的基本信息。

            GET /users/:login
            # 或
            GET /users/:id
            :param id:
            :param login:
            :return:
            """
            if is_blank(id) and is_blank(login):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_users", p1="id", p2="login",
                                                    doc_uri="https://www.yuque.com/yuque/developer/user")
                raise YuQueAPIException(message)
            return self.yuque_api.get_request(source_name="users/{}".format(id if is_not_blank(id) else login),
                                              res_type=UserSerializer)

        def get_user_docs(self, q: str = "", offset: int = 1) -> Optional[DocSerializerList]:
            """
            获取我创建的文档

            :param q:       文档标题模糊搜索
            :param offset:  用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :return:         Optional[DocSerializerList]
            """
            params = {"q": q, "offset": offset}
            return self.yuque_api.get_request(source_name="/user/docs",
                                              res_type=DocSerializerList,
                                              params=params)

        def get_user_recent_updated(self,
                                    type: Union[UserDescriptionType, str] = UserDescriptionType.BOOK,
                                    offset: int = 1) -> Optional[Union[DocSerializerList, BookSerializerList]]:
            """
            获取我最近参与的文档/知识库

            :param type:        Doc - 文档,Book - 知识库
            :param offset:      用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :return:            Optional[Union[DocSerializerList, BookSerializerList]]
            """
            params = {"type": type.value if isinstance(type, UserDescriptionType) else
            type[0].upper() + str(type[1:len(type)]).lower(), "offset": offset}
            res = self.yuque_api.get_request(source_name="/user/recent-updated",
                                             res_type=None, params=params)
            if res is None:
                return res
            if type == UserDescriptionType.DOC:
                return DocSerializerList(base_response=res)
            elif type == UserDescriptionType.BOOK:
                return BookSerializerList(base_response=res)
            return None

    # Group - 组织
    # @See https://www.yuque.com/yuque/developer/group
    class Group(BaseRelation):
        def get_users_groups(self,
                             login: str = None,
                             id: int = None) -> Optional[UserSerializerList]:
            """
            获取某个用户的加入的组织列表

            :param login:
            :param id:
            :return:
            """
            if is_blank(id) and is_blank(login):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_users_groups", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            return self.yuque_api.get_request(
                source_name="/users/{}/groups".format(login if is_not_blank(login) else id),
                res_type=UserSerializerList)

        def get_public_groups(self) -> Optional[UserSerializerList]:
            """
            获取公开组织列表
            :return:
            """
            return self.yuque_api.get_request(source_name="/groups", res_type=UserSerializerList)

        @property
        def public_groups(self) -> Optional[UserSerializerList]:
            return self.get_public_groups()

        def post_group(self, name: str, login: str, description: str = "") -> Optional[UserSerializer]:
            """
            创建 Group
            :param name:            组织名称
            :param login:           login 访问后缀
            :param description:     描述
            :return:
            """
            if is_blank(name):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_group", p1="name",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            if is_blank(login):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_group", p1="login",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)

            data = {"name": name, "login": login, "description": description}
            return self.yuque_api.post_request(source_name="/groups",
                                               res_type=UserSerializer,
                                               data=data)

        def create_group(self, **kwargs) -> Optional[UserSerializer]:
            return self.post_group(**kwargs)

        def get_groups_detail(self, id: int = None, login: str = None) -> Optional[UserSerializer]:
            """
            获取单个组织的详细信息
            GET /groups/:login
            # 或
            GET /groups/:id
            :param id:
            :param login:
            :return: Optional[UserSerializer]
            """
            if is_blank(id) and is_blank(login):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_groups", p1="id", p2="login",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            return self.yuque_api.get_request(source_name="/groups/{}".format(id if is_not_blank(id) else login),
                                              res_type=UserSerializer)

        def put_groups(self,
                       login: str = None,
                       id: int = None,
                       name: str = None,
                       login_update: str = None,
                       description: str = "") -> Optional[UserSerializer]:
            """
            更新单个组织的详细信息

            PUT /groups/:login
            # 或
            PUT /groups/:id
            :param login:
            :param id:
            :param name:
            :param login_update:
            :param description:
            :return:
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="put_groups", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            data = {"name": name, "login": login_update, "description": description}
            return self.yuque_api.put_request(source_name="/groups/{}".format(login if is_not_blank(login) else id),
                                              res_type=UserSerializer, data=data)

        def update_groups(self, **kwargs) -> Optional[UserSerializer]:
            return self.put_groups(**kwargs)

        def delete_groups(self, login: str = None, id: int = None):
            """
            删除组织
            DELETE /groups/:login
            # 或
            DELETE /groups/:id
            :param login:
            :param id:
            :return:
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="delete_groups", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)

            return self.yuque_api.delete_request(source_name="/groups/{}".format(login if is_not_blank(login) else id),
                                                 res_type=UserSerializer)

        def get_groups_users(self, login: str = None, id: int = None) -> Optional[GroupUserSerializerList]:
            """
            获取组织成员信息
            GET /groups/:login/users
            # 或
            GET /groups/:id/users
            :param login:
            :param id:
            :return:
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_groups_users", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)

            return self.yuque_api.get_request(
                source_name="/groups/{}/users".format(login if is_not_blank(login) else id),
                res_type=GroupUserSerializerList)

        def put_groups_users(self,
                             group_login: str = None,
                             group_id: int = None,
                             login: str = None,
                             role: Union[int, GroupUserRole] = GroupUserRole.USER) -> Optional[GroupUserSerializer]:

            """
            增加或更新组织成员

            PUT /groups/:group_login/users/:login
            # 或
            PUT /groups/:group_id/users/:login
            :param role:                0 - 管理员, 1 - 普通成员
            :param group_login:
            :param group_id:
            :param login:
            :return:
            """
            if is_blank(group_login) and is_blank(group_id):
                message = MESSAGE_TEMPLATE_A.format(method_name="put_groups_users", p1="group_login", p2="group_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            if is_blank(login):
                message = MESSAGE_TEMPLATE_B.format(method_name="put_groups_users", p1="login",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            data = {"role": role.value if isinstance(role, GroupUserRole) else role}
            return self.yuque_api.put_request(
                source_name="/groups/{0}/users/{1}".format(group_login if is_not_blank(group_login) else group_id,
                                                           login),
                res_type=GroupUserSerializer,
                data=data)

        def update_group_users(self, **kwargs):
            return self.put_groups_users(**kwargs)

        def delete_groups_users(self,
                                group_login: str = None,
                                group_id: int = None,
                                login: str = None) -> Optional[GroupUserSerializer]:

            """
            删除组织成员
            PUT /groups/:group_login/users/:login
            # 或
            PUT /groups/:group_id/users/:login
            :param group_login:
            :param group_id:
            :param login:
            :return:
            """
            if is_blank(group_login) and is_blank(group_id):
                message = MESSAGE_TEMPLATE_A.format(method_name="delete_groups_users", p1="group_login", p2="group_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)
            if is_blank(login):
                message = MESSAGE_TEMPLATE_B.format(method_name="delete_groups_users", p1="login",
                                                    doc_uri="https://www.yuque.com/yuque/developer/group")
                raise YuQueAPIException(message)

            return self.yuque_api.delete_request(
                source_name="/groups/{0}/users/{1}".format(group_login if is_not_blank(group_login) else group_id,
                                                           login),
                res_type=GroupUserSerializer)

    # Repo - 知识库
    # @See https://www.yuque.com/yuque/developer/repo
    class Repo(BaseRelation):
        def get_users_repos(self,
                            type: Union[RepoType, str] = RepoType.ALL,
                            include_membered: bool = False,
                            offset: int = 0,
                            login: str = None,
                            id: int = None) -> Optional[BookSerializerList]:
            """
            获取某个用户知识库列表
            # for User
            GET /users/:login/repos
            GET /users/:id/repos

            :param type:                Book, Design, all - 所有类型
            :param include_membered:    true 包含用户参加的知识库，false 只返回用户创建的
            :param offset:              用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :param login:               username , 用户名称
            :param id:                  userid   , 用户Id
            :return:                    Optional[BookSerializerList]
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_users_repos", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)
            params = {"type": type.value,
                      "offset": offset,
                      'include_membered': include_membered}
            return self.yuque_api.get_request(
                source_name="/users/{}/repos".format(login if is_not_blank(login) else id),
                res_type=BookSerializerList,
                params=params)

        def get_group_repos(self,
                            type: Union[RepoType, str] = RepoType.ALL,
                            include_membered: bool = False,
                            offset: int = 1,
                            login: str = None,
                            id: int = None) -> Optional[BookSerializerList]:
            """
            获取某个团队的知识库列表
            GET /groups/:login/repos
            GET /groups/:id/repos

            :param type:                Book, Design, all - 所有类型
            :param include_membered:    true 包含用户参加的知识库，false 只返回用户创建的
            :param offset:              用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :param login:               团队名称
            :param id:                  段对Id
            :return:                    Optional[BookSerializerList]
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_group_repos", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)
            return self.get_users_repos(type=type, include_membered=include_membered, offset=offset, login=login, id=id)

        def post_users_repos(self, name: str,
                             slug: str,
                             description: str = "",
                             public: Union[RepoPublic, int] = RepoPublic.PRIVATE,
                             type: Union[RepoType, str] = RepoType.BOOK,
                             login: str = None,
                             id: int = None) -> Optional[BookSerializer]:
            """
            创建知识库
            往自己下面创建知识库
            POST /users/:login/repos
            POST /users/:id/repos

            :param name:            知识库名称
            :param slug:            slug
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param type:            ‘Book’ 文库, ‘Design’ 画板, 请注意大小写
            :param login:           用户名称
            :param id:              用户Id
            :return:                Optional[BookSerializer]
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="post_users_repos", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            if is_blank(name):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_users_repos", p1="name",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)
            if is_blank(slug):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_users_repos", p1="slug",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            data = {"name": name, "slug": slug, "description": description, "public": public.value, "type": type.value}
            book_serializer = self.yuque_api.post_request(
                source_name="/groups/{}/repos".format(login if is_not_blank(login) else id),
                res_type=BookSerializer, data=data)
            return book_serializer

        def post_groups_repos(self,
                              name: str,
                              slug: str,
                              description: str = "",
                              public: Union[RepoPublic, int] = RepoPublic.PRIVATE,
                              type: Union[RepoType, str] = RepoType.BOOK,
                              login: str = None,
                              id: int = None) -> Optional[BookSerializer]:
            """
            创建新知识库
            往团队创建知识库
            POST /groups/:login/repos
            POST /groups/:id/repos
            :param name:            知识库名称
            :param slug:            slug
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param type:            ‘Book’ 文库, ‘Design’ 画板, 请注意大小写
            :param login:           团队名称
            :param id:              团队Id
            :return:                Optional[BookSerializer]
            """
            if is_blank(login) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="post_groups_repos", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            if is_blank(name):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_groups_repos", p1="name",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)
            if is_blank(slug):
                message = MESSAGE_TEMPLATE_B.format(method_name="post_groups_repos", p1="slug",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            book_serializer = self.post_users_repos(name=name, slug=slug, description=description, public=public,
                                                    type=type,
                                                    login=login,
                                                    id=id)
            if book_serializer is None:
                return book_serializer

            if is_not_blank(login):
                book_serializer.web_link = "{0}/{1}/{2}".format(YUQUE_MAIN_URL, login, book_serializer.slug)

            return book_serializer

        def get_repos(self,
                      namespace: str = None,
                      id: int = None,
                      type: Union[str, RepoType] = RepoType.BOOK) -> Optional[BookDetailSerializer]:
            """
            获取知识库详情
            GET /repos/:namespace
            # 或
            GET /repos/:id
            :param namespace:
            :param id:
            :param type:        知识库类型，Book - 文库，Design - 设计稿
            :return:            Optional[BookDetailSerializer]
            """
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="get_repos", p1="login", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            params = {"type": type.value if isinstance(type, RepoType) else type}
            return self.yuque_api.get_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDetailSerializer,
                params=params)

        def put_repos(self,
                      name: str = None,
                      slug: str = None,
                      toc: str = None,
                      description: str = None,
                      public: Union[int, RepoPublic] = RepoPublic.PRIVATE,
                      namespace: str = None, id: int = None, ) -> Optional[BookDetailSerializer]:

            """
            更新知识库信息

            :param name:            知识库名称
            :param slug:             slug
            :param toc:             更新文档知识库的目录信息
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param namespace:
            :param id:
            :return:                Optional[BookDetailSerializer]
            """
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="put_repos", p1="namespace", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            data = {}
            if name is not None:
                data["name"] = name
            if slug is not None:
                data['slug'] = slug
            if toc is not None:
                data['toc'] = toc

            if description is not None:
                data['description'] = description

            data['public'] = public.value if isinstance(public, RepoPublic) else public

            return self.yuque_api.put_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDetailSerializer,
                data=data)

        def delete_repo(self, namespace: str = None, id: int = None) -> Optional[BookDeleteSerializer]:
            """
            删除知识库
            DELETE /repos/:namespace
            # 或
            DELETE /repos/:id
            :param namespace:
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="delete_repo", p1="namespace", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            return self.yuque_api.delete_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDeleteSerializer)

        def repos_toc(self, namespace: str = None, id: int = None) -> Optional[RepoTocSerializerList]:
            """
            获取一个知识库的目录结构
            GET /repos/:namespace/toc
            # 或
            GET /repos/:id/toc

            :param namespace:
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_toc", p1="namespace", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            return self.yuque_api.get_request(
                source_name="/repos/{}/toc".format(namespace if is_not_blank(namespace) else id),
                res_type=RepoTocSerializerList)

        def search_repos(self, q: str, type: Union[str, RepoType] = RepoType.BOOK) -> Optional[BookSerializerList]:
            """
            基于关键字搜索知识库
            GET /search/repos?q=&type=
            :param q:       关键字，目前是简单的数据库模糊查询
            :param type:    类型 (Book, Design），注意大小写，不传搜索所有类型
            :return:        Optional[BookSerializerList]
            """
            if is_blank(q):
                message = MESSAGE_TEMPLATE_B.format(method_name="search_repos", p1="q",
                                                    doc_uri="https://www.yuque.com/yuque/developer/repo")
                raise YuQueAPIException(message)

            params = {"q": q, "type": type.value if isinstance(type, RepoType) else type}
            return self.yuque_api.get_request(source_name="/search/repos", res_type=BookSerializerList, params=params)

        def get_repo(self, **kwargs) -> Optional[BookSerializerList]:
            """
            获取用户或者企业知识库
            :param kwargs:
            :return:
            """
            return self.get_users_repos(**kwargs)

        def get_repos_detail(self, **kwargs) -> Optional[BookDetailSerializer]:
            """
            获取知识库详情
            :param kwargs:
            :return:
            """
            return self.get_repos(**kwargs)

        def create_repos(self, **kwargs) -> Optional[BookSerializer]:
            """
            创建知识库
            :param kwargs:
            :return:
            """
            return self.post_users_repos(**kwargs)

        def update_repos(self, **kwargs) -> Optional[BookDetailSerializer]:
            """
            更新知识库
            :param kwargs:
            :return:
            """
            return self.put_repos(**kwargs)

    # Doc - 文档
    # @See https://www.yuque.com/yuque/developer/doc
    class Doc(BaseRelation):
        def get_repos_docs(self,
                           namespace: str = None,
                           id: int = None) -> Optional[DocSerializerList]:
            """
            获取知识库下的文档
            :param namespace:
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(id):
                raise YuQueAPIException("#repo_docs , namespace and id can not both be blank !")
            return self.yuque_api.get_request(
                source_name="/repos/{}/docs".format(namespace if is_not_blank(namespace) else id),
                res_type=DocSerializerList)

        def get_repos_docs_detail(self,
                                  namespace: str = None,
                                  slug: str = None,
                                  repo_id: str = None,
                                  id: int = None,
                                  raw: Union[int, DocRaw] = DocRaw.MARKDOWN) -> Optional[DocDetailSerializer]:
            """
            获取单篇文档的详细信息
            GET /repos/:namespace/docs/:slug
            # 或
            GET /repos/:repo_id/docs/:id

            :param namespace:
            :param slug:
            :param repo_id:
            :param id:
            :param raw: 	raw=1 返回 Markdown 格式文本； 其他则返回 HTML 格式的富文本
            :return:
            """
            if is_blank(namespace) and is_blank(repo_id):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_docs_detail",
                                                    p1="namespace", p2="repo_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            if is_blank(slug) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_docs_detail",
                                                    p1="slug", p2="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            if is_not_blank(namespace) and is_blank(slug):
                message = MESSAGE_TEMPLATE_B.format(method_name="repos_docs_detail",
                                                    p1="slug",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            if is_not_blank(repo_id) and is_blank(id):
                message = MESSAGE_TEMPLATE_B.format(method_name="repos_docs_detail",
                                                    p1="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            params = {"raw": raw.value if isinstance(raw, DocRaw) else raw}
            if is_not_blank(namespace):
                return self.yuque_api.get_request(source_name="/repos/{0}/docs/{1}".format(namespace, slug),
                                                  res_type=DocDetailSerializer,
                                                  params=params)
            return self.yuque_api.get_request(source_name="/repos/{0}/docs/{1}".format(repo_id, id),
                                              res_type=DocDetailSerializer,
                                              params=params)

        def get_docs_detail(self, **kwargs) -> Optional[DocDetailSerializer]:
            return self.get_repos_docs_detail(**kwargs)

        def post_repos_docs(self, namespace: str = None,
                            id: int = None,
                            title: str = None,
                            slug: str = None,
                            public: Union[DocPublic, int] = DocPublic.PRIVATE,
                            body: str = None) -> \
                Optional[DocDetailSerializer]:
            """
            创建文档
            POST /repos/:namespace/docs
            # 或
            POST /repos/:id/docs
            :param namespace:
            :param id:
            :param title:       标题
            :param slug:        文档 Slug
            :param public:      0 - 私密 ,1 - 公开
            :param body:        已发布的正文 Markdown
            :return:            DocDetailSerializer
            """
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="post_repos_docs", p1="namespace", p2="repo_id",
                                                    doc_uri='https://www.yuque.com/yuque/developer/doc')
                raise YuQueAPIException(message)

            data = {"title": title, "slug": slug, "public": public.value if isinstance(public, DocPublic) else public,
                    "body": body}
            return self.yuque_api.post_request(
                source_name="/repos/{}/docs".format(namespace if is_not_blank(namespace) else id),
                res_type=DocDetailSerializer, data=data)

        def create_docs(self, **kwargs) -> Optional[DocDetailSerializer]:
            return self.post_repos_docs(**kwargs)

        def put_repos_docs(self, namespace: str = None,
                           repo_id: int = None,
                           id: int = None,
                           title: str = None,
                           slug: str = None,
                           public: Union[DocPublic, int] = DocPublic.PRIVATE,
                           body: str = None) -> \
                Optional[DocDetailSerializer]:
            """
            PUT /repos/:namespace/docs/:id
            # 或
            PUT /repos/:repo_id/docs/:id
            :param namespace:
            :param repo_id:
            :param id:
            :param title:       标题
            :param slug:        文档 Slug
            :param public:      0 - 私密 , 1 - 公开
            :param body:        已发布的正文 Markdown
            :return:            Optional[DocDetailSerializer]

            注意! 这里最后个参数是 id （文档编号）而不是 slug，原因是为了避免 slug 改变无法正确保存。
            """
            if is_blank(namespace) and is_blank(repo_id):
                message = MESSAGE_TEMPLATE_A.format(method_name="put_repos_docs", p1="namespace", p2="repo_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)
            if is_blank(id):
                message = MESSAGE_TEMPLATE_B.format(method_name="put_repos_docs", p1="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            data = {"title": title, "slug": slug, "public": public.value if isinstance(public, DocPublic) else public,
                    "body": body}

            return self.yuque_api.put_request(
                source_name="/repos/{0}/docs/{1}".format(namespace if is_not_blank(namespace) else repo_id, id),
                res_type=DocDetailSerializer,
                data=data)

        def update_docs(self, **kwargs) -> Optional[DocDetailSerializer]:
            return self.put_repos_docs(**kwargs)

        def delete_repos_docs(self,
                              namespace: str = None,
                              repo_id: int = None,
                              id: int = None) -> Optional[DocDetailSerializer]:
            """
            删除文档

            DELETE /repos/:namespace/docs/:id
            # 或
            DELETE /repos/:repo_id/docs/:id
            :param namespace:
            :param repo_id
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(repo_id):
                message = MESSAGE_TEMPLATE_A.format(method_name="delete_repos_docs", p1="namespace", p2="repo_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)
            if is_blank(id):
                message = MESSAGE_TEMPLATE_B.format(method_name="delete_repos_docs", p1="id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            return self.yuque_api.delete_request(
                source_name="repos/{0}/docs/{1}".format(namespace if is_not_blank(namespace) else repo_id, id),
                res_type=DocDetailSerializer)

        def delete_docs(self, **kwargs) -> Optional[DocDetailSerializer]:
            return self.delete_repos_docs(**kwargs)


# 快速管理
class SimplePyYuQueQuickAPI(SimplePyYuQueAPI):
    def __init__(self, token: str, app_name: str, **kwargs):
        super().__init__(token, app_name, **kwargs)
        self._quick_user_structure = QuickUserStructure()
        self._build()

    @property
    def user_structure(self) -> Optional[UserSerializer]:
        return self._quick_user_structure.user_serializer

    @property
    def user_repo_structure_list(self) -> List[QuickRepoStructure]:
        return self._quick_user_structure.quick_repo_structure_list or []

    @property
    def user_doc_structure_list(self) -> List[QuickDocStructure]:
        return [] if is_blank(self._quick_user_structure.quick_repo_structure_list) \
            else [doc.quick_doc_structure_list for doc in
                  self._quick_user_structure.quick_repo_structure_list]

    @property
    def group_structure_list(self) -> List[QuickGroupStructure]:
        return self._quick_user_structure.quick_group_structure_list

    @property
    def group_repo_structure_list(self) -> List[QuickRepoStructure]:
        return [] if is_blank(self._quick_user_structure.quick_group_structure_list) else \
            [group.quick_repo_structure_list for group in self._quick_user_structure.quick_group_structure_list]

    @property
    def group_doc_structure_list(self) -> List[QuickDocStructure]:
        if is_blank(self._quick_user_structure.quick_group_structure_list):
            return []
        repo_list = [group.quick_repo_structure_list for group in self._quick_user_structure.quick_group_structure_list]
        if is_blank(repo_list):
            return []
        return [doc.quick_doc_structure_list for doc in repo_list]

    def at_user(self, login: str = None, id: int = None):
        if is_blank(login) and is_blank(id):
            user_serializer = self.User().user
        else:
            user_serializer = self.User().get_users(id=id)
        self._quick_user_structure.user_serializer = user_serializer
        return self

    def at_user_repo(self, login: str = None, id: int = None):
        if is_blank(login) and is_blank(id):
            repo_list = self.Repo().get_users_repos(
                id=self._quick_user_structure.user_serializer.id).book_serializer_list
        else:
            repo_list = self.Repo().get_users_repos(login=login, id=id).book_serializer_list
        if repo_list is None:
            return self

        quick_repo_list = []
        for repo in repo_list:
            repo_detail = self.Repo().get_repos(id=repo.id)
            quick_repo = QuickRepoStructure(repo_detail_serializer=repo_detail, repo_serializer=repo)
            quick_repo_list.append(quick_repo)

        self._quick_user_structure.quick_repo_structure_list = repo_list
        return self

    def at_user_doc(self):
        pass

    def at_group(self):
        pass

    def at_group_repo(self):
        pass

    def at_group_doc(self):
        pass

    def _build(self):
        quick_user = self._quick_user_structure or QuickUserStructure()
        quick_user.user_serializer = self.User().user
        # TODO
        # 团队

        # 个人
        repo_list = self.Repo().get_users_repos(login=self.User().user.name,
                                                id=self.User().user.id).book_serializer_list
        quick_repo_list = []
        for repo in repo_list:
            print("Repo基础")
            print(repo.base_response)
            repo_detail = self.Repo().get_repos(id=repo.id)
            print("Repo详细")
            print(repo_detail.base_response)
            quick_repo = QuickRepoStructure(repo_detail_serializer=repo_detail, repo_serializer=repo)
            quick_repo_list.append(quick_repo)

            doc_list = self.Doc().get_repos_docs(id=repo.id).doc_serializer_list
            quick_doc_list = []
            for doc in doc_list:
                print("Doc基础")
                print(doc.base_response)
                doc_detail = self.Doc().get_repos_docs_detail(id=doc.id, repo_id=repo.id)
                print("Doc详细")
                print(doc_detail.base_response)

                quick_doc = QuickDocStructure(doc_serializer=doc, doc_detail_serializer=doc_detail)
                quick_doc_list.append(quick_doc)
            quick_repo.quick_doc_structure_list = quick_doc_list

        quick_user.quick_repo_structure_list = quick_repo_list
        self._quick_user_structure = quick_user
        return self
