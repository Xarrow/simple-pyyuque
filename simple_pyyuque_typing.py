# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_typing.py
 Time: 2019/12/19
"""
from typing import Optional, Union, List
from enum import Enum

YUQUE_MAIN_URL = "https://www.yuque.com/"

STATUS_CODE_MAPPING = {
    200: "成功",
    400: "请求的参数不正确，或缺少必要信息，请对比文档",
    401: "需要用户认证的接口用户信息不正确",
    403: "缺少对应功能的权限",
    404: "数据不存在，或未开放",
    500: "服务器异常",
}


class StatusCode(Enum):
    SUCCESS = {"code": 200, "message": "成功", }
    PARAMETERS_ERROR = {"code": 400, "message": "请求的参数不正确，或缺少必要信息，请对比文档", }
    AUTH_ERROR = {"code": 401, "message": "需要用户认证的接口用户信息不正确", }
    PERMISSION_ERROR = {"code": 403, "message": "缺少对应功能的权限", }
    DATA_NOT_RELEASE = {"code": 404, "message": "数据不存在，或未开放", }
    SERVER_OPS = {"code": 500, "message": "服务器异常", }


class RequestMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


class UserDescriptionType(Enum):
    # Doc - 文档
    DOC = "Doc"
    # Book - 知识库
    BOOK = "Book"


class GroupUserRole(Enum):
    # 0 - 管理员, 1 - 普通成员
    ADMINISTRATOR = 0
    USER = 1


class RepoType(Enum):
    BOOK = "Book"
    DESIGN = "Design"
    ALL = "all"


class RepoPublic(Enum):
    PRIVATE = 1
    INTERNAL_OPEN = 2
    ALL_OPEN = 3


class DocPublic(Enum):
    PRIVATE = 0
    OPEN = 1


class DocRaw(Enum):
    # raw=1 返回 Markdown 格式文本；其他则返回 HTML 格式的富文本
    MARKDOWN = 1
    HTMl = 2


class BaseSerializer(object):
    __slots__ = ['_base_response', '_web_link']

    def __init__(self, base_response: dict):
        self._base_response = base_response
        self._web_link = ""

    @property
    def base_response(self) -> Optional[dict]:
        return self._base_response

    @base_response.setter
    def base_response(self, value: dict):
        self._base_response = value

    @property
    def serializer(self) -> Optional[str]:
        if isinstance(self.base_response, dict):
            return self.base_response.get("_serializer") if self.base_response is not None else None
        return None

    # TODO
    @property
    def abilities(self) -> Optional[dict]:
        return None

    @property
    def update(self) -> Optional[bool]:
        return None if self.abilities is None else self.abilities.get("update")

    @property
    def destroy(self) -> Optional[bool]:
        return None if self.abilities is None else self.abilities.get("destroy")

    @property
    def web_link(self):
        return self._web_link

    @web_link.setter
    def web_link(self, web_link):
        self._web_link = web_link


class UserSerializer(BaseSerializer):
    """
    UserSerializer @See https://www.yuque.com/yuque/developer/userserializer
    """

    def __init__(self, user_response: dict) -> None:
        super().__init__(user_response)

    @property
    def user_response(self) -> Optional[dict]:
        return self.base_response

    @user_response.setter
    def user_response(self, value: dict):
        self.base_response = value

    @property
    def id(self) -> Optional[int]:
        return self.user_response.get('id') if self.user_response is not None else None

    @property
    def type(self):
        return self.user_response.get('type') if self.user_response is not None else None

    @property
    def space_id(self):
        return self.user_response.get('space_id') if self.user_response is not None else None

    @property
    def account_id(self):
        return self.user_response.get('account_id') if self.user_response is not None else None

    @property
    def login(self):
        return self.user_response.get('login') if self.user_response is not None else None

    @property
    def name(self):
        return self.user_response.get('name') if self.user_response is not None else None

    @property
    def description(self):
        return self.user_response.get('description') if self.user_response is not None else None

    @property
    def avatar_url(self):
        return self.user_response.get('avatar_url') if self.user_response is not None else None

    @property
    def large_avatar_url(self):
        return self.user_response.get('large_avatar_url') if self.user_response is not None else None

    @property
    def medium_avatar_url(self):
        return self.user_response.get('medium_avatar_url') if self.user_response is not None else None

    @property
    def small_avatar_url(self):
        return self.user_response.get('small_avatar_url') if self.user_response is not None else None

    @property
    def book_count(self):
        return self.user_response.get('book_count') if self.user_response is not None else None

    @property
    def public_books_count(self):
        return self.user_response.get('public_books_count') if self.user_response is not None else None

    @property
    def follower_count(self):
        return self.user_response.get('follower_count') if self.user_response is not None else None

    @property
    def following_count(self):
        return self.user_response.get('following_count') if self.user_response is not None else None

    @property
    def public(self):
        return self.user_response.get('public') if self.user_response is not None else None

    @property
    def created_at(self):
        return self.user_response.get('created_at') if self.user_response is not None else None

    @property
    def updated_at(self):
        return self.user_response.get('updated_at') if self.user_response is not None else None

    @property
    def web_link(self):
        if self.name is None:
            return None
        return "{0}/{1}".format(YUQUE_MAIN_URL, self.login)

    def __repr__(self):
        return 'UserSerializer=(id={!r},type={!r},{!r} ,description={!r},acatar_url={!r},created_at={!r},upadate_at={' \
               '!r},)'.format(self.id, self.type, self.name, self.description, self.avatar_url, self.created_at,
                              self.updated_at)


class BookSerializer(BaseSerializer):
    """
    @See https://www.yuque.com/yuque/developer/bookserializer

    """

    def __init__(self, book_response: dict):
        super().__init__(book_response)

    @property
    def book_response(self) -> Optional[dict]:
        return self.base_response

    @book_response.setter
    def book_response(self, value) -> None:
        self.base_response = value

    # id - 仓库编号
    @property
    def id(self) -> Optional[int]:
        return self.base_response.get("id") if self.base_response is not None else None

    # type - 类型 [Book - 文档]
    @property
    def type(self) -> Optional[str]:
        return self.base_response.get("type") if self.base_response is not None else None

    # slug - 仓库路径
    @property
    def slug(self) -> Optional[int]:
        return self.base_response.get("slug") if self.base_response is not None else None

    # name - 名称
    @property
    def name(self) -> Optional[int]:
        return self.base_response.get("name") if self.base_response is not None else None

    # namespace - 仓库完整路径 user.login/book.slug
    @property
    def namespace(self) -> Optional[str]:
        return self.base_response.get("namespace") if self.base_response is not None else None

    # user - <UserSerializer>
    @property
    def user_id(self) -> Optional[str]:
        return self.base_response.get("user_id") if self.base_response is not None else None

    @property
    def user(self) -> UserSerializer:
        return UserSerializer(user_response=self.base_response.get("user")) if self.base_response is not None else None

    # description - 介绍
    @property
    def description(self) -> Optional[str]:
        return self.base_response.get("description") if self.base_response is not None else None

    # creator_id - 创建人 User Id
    @property
    def creator_id(self) -> Optional[int]:
        return self.base_response.get("creator_id") if self.base_response is not None else None

    # public - 公开状态 [1 - 公开, 0 - 私密]
    @property
    def public(self) -> Optional[int]:
        return self.base_response.get("public") if self.base_response is not None else None

    # likes_count - 喜欢数量
    @property
    def likes_count(self) -> Optional[int]:
        return self.base_response.get("likes_count") if self.base_response is not None else None

    # watches_count - 订阅数量
    @property
    def watches_count(self) -> Optional[int]:
        return self.base_response.get("watches_count") if self.base_response is not None else None

    @property
    def content_updated_at(self) -> Optional[str]:
        return self.base_response.get("content_updated_at") if self.base_response is not None else None

    # updated_at - 更新时间
    @property
    def updated_at(self) -> Optional[str]:
        return self.base_response.get("updated_at") if self.base_response is not None else None

    # created_at - 创建时间
    @property
    def created_at(self) -> Optional[str]:
        return self.base_response.get("created_at") if self.base_response is not None else None

    @property
    def user_login(self) -> Optional[int]:
        return self.base_response.get("user.login") if self.base_response is not None else None

    @property
    def web_link(self):
        if self.namespace is None:
            return None
        return "{0}/{1}".format(YUQUE_MAIN_URL, self.namespace)

    # TODO
    def __repr__(self):
        return "BookSerializer=(id={!r} ......)".format(self.id)


class BookDetailSerializer(BaseSerializer):
    """
    @See https://www.yuque.com/yuque/developer/bookdetailserializer

    """

    def __init__(self, book_detail_response: dict):
        super().__init__(book_detail_response)

    @property
    def book_detail_response(self) -> Optional[dict]:
        return self.base_response

    @book_detail_response.setter
    def book_detail_response(self, value) -> None:
        self.base_response = value

    # id - 文档编号
    @property
    def id(self) -> Optional[int]:
        return self.base_response.get("id") if self.base_response is not None else None

    # slug - 文档路径
    @property
    def slug(self) -> Optional[str]:
        return self.base_response.get("slug") if self.base_response is not None else None

    # title - 标题
    @property
    def title(self) -> Optional[str]:
        return self.base_response.get("title") if self.base_response is not None else None

    # book_id - 仓库编号，就是 repo_id
    @property
    def book_id(self) -> Optional[str]:
        return self.base_response.get("book_id") if self.base_response is not None else None

    # book - 仓库信息 <BookSerializer>，就是 repo 信息
    @property
    def book(self) -> Optional[BookSerializer]:
        return BookSerializer(book_response=self.base_response.get("book")) if self.base_response is not None else None

    # user_id - 用户/团队编号
    @property
    def user_id(self) -> Optional[str]:
        return self.base_response.get("user_id") if self.base_response is not None else None

    # user - 用户/团队信息 <UserSerializer>
    @property
    def user(self) -> Optional[str]:
        return self.base_response.get("user") if self.base_response is not None else None

    # format - 描述了正文的格式 [asl , markdown]
    @property
    def format(self) -> Optional[str]:
        return self.base_response.get("format") if self.base_response is not None else None

    # body - 正文 Markdown 源代码 format = markdown，正文在这个字段里面
    @property
    def body(self) -> Optional[str]:
        return self.base_response.get("body") if self.base_response is not None else None

    # body_asl - 正文 ASL 源代码 format = asl，正文在这个字段里面
    @property
    def body_asl(self) -> Optional[str]:
        return self.base_response.get("body_asl") if self.base_response is not None else None

    # body_draft - 草稿 Markdown, format = markdown
    @property
    def body_draft(self) -> Optional[str]:
        return self.base_response.get("body_draft") if self.base_response is not None else None

    # body_draft_asl - 草稿 ASL, format = asl
    @property
    def body_draft_asl(self) -> Optional[str]:
        return self.base_response.get("body_draft_asl") if self.base_response is not None else None

    # body_html - 基于 Markdown/ASL 转换过后的正文 HTML
    @property
    def body_html(self) -> Optional[str]:
        return self.base_response.get("body_html") if self.base_response is not None else None

    # creator_id - 文档创建人 User Id
    @property
    def creator_id(self) -> Optional[str]:
        return UserSerializer(
            user_response=self.base_response.get("creator_id")) if self.base_response is not None else None

    # public - 公开级别 [0 - 私密, 1 - 公开]
    @property
    def public(self) -> Optional[int]:
        return self.base_response.get("public") if self.base_response is not None else None

    # status - 状态 [0 - 草稿, 1 - 发布]
    @property
    def status(self) -> Optional[int]:
        return self.base_response.get("status") if self.base_response is not None else None

    # likes_count - 赞数量
    @property
    def likes_count(self) -> Optional[int]:
        return self.base_response.get("likes_count") if self.base_response is not None else None

    # comments_count - 评论数量
    @property
    def comments_count(self) -> Optional[int]:
        return self.base_response.get("name") if self.base_response is not None else None

    # content_updated_at - 文档内容更新时间
    @property
    def content_updated_at(self) -> Optional[str]:
        return self.base_response.get("content_updated_at") if self.base_response is not None else None

    # deleted_at - 删除时间，未删除为 Null
    @property
    def deleted_at(self) -> Optional[str]:
        return self.base_response.get("deleted_at") if self.base_response is not None else None

    # created_at - 创建时间
    @property
    def created_at(self) -> Optional[int]:
        return self.base_response.get("created_at") if self.base_response is not None else None

    # updated_at - 更新时间
    @property
    def updated_at(self) -> Optional[str]:
        return self.base_response.get("updated_at") if self.base_response is not None else None

    def __repr__(self):
        return "BookSerializer=(id={!r} ......)".format(self.id)


class BookDeleteSerializer(BaseSerializer):
    def __init__(self, book_delete_response: dict):
        super().__init__(book_delete_response)

    @property
    def book_delete_response(self) -> Optional[dict]:
        return self.book_delete_response

    @book_delete_response.setter
    def book_delete_response(self, value) -> None:
        self.book_delete_response = value

    @property
    def id(self) -> Optional[int]:
        return self.base_response.get('id') if self.base_response is not None else None

    @property
    def type(self) -> Optional[str]:
        return self.base_response.get('type') if self.base_response is not None else None

    @property
    def slug(self) -> Optional[str]:
        return self.base_response.get('slug') if self.base_response is not None else None

    @property
    def name(self) -> Optional[str]:
        return self.base_response.get('name') if self.base_response is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.base_response.get('user_id') if self.base_response is not None else None

    @property
    def description(self) -> Optional[str]:
        return self.base_response.get('description') if self.base_response is not None else None

    @property
    def toc(self) -> Optional[str]:
        return self.base_response.get('toc') if self.base_response is not None else None

    @property
    def toc_yml(self) -> Optional[str]:
        return self.base_response.get('toc_yml') if self.base_response is not None else None

    @property
    def creator_id(self) -> Optional[int]:
        return self.base_response.get('creator_id') if self.base_response is not None else None

    @property
    def public(self) -> Optional[int]:
        return self.base_response.get('public') if self.base_response is not None else None

    @property
    def items_count(self) -> Optional[int]:
        return self.base_response.get('items_count') if self.base_response is not None else None

    @property
    def likes_count(self) -> Optional[int]:
        return self.base_response.get('likes_count') if self.base_response is not None else None

    @property
    def watches_count(self) -> Optional[int]:
        return self.base_response.get('watches_count') if self.base_response is not None else None

    @property
    def pinned_at(self) -> Optional[str]:
        return self.base_response.get('pinned_at') if self.base_response is not None else None

    @property
    def archived_at(self) -> Optional[str]:
        return self.base_response.get('archived_at') if self.base_response is not None else None

    @property
    def namespace(self) -> Optional[str]:
        return self.base_response.get('namespace') if self.base_response is not None else None

    @property
    def user(self) -> Optional[UserSerializer]:
        return UserSerializer(user_response=self.base_response.get('user')) if self.base_response is not None else None

    @property
    def created_at(self) -> Optional[str]:
        return self.base_response.get('created_at') if self.base_response is not None else None

    @property
    def updated_at(self) -> Optional[str]:
        return self.base_response.get('updated_at') if self.base_response is not None else None

    @property
    def _serializer(self) -> Optional[str]:
        return self.base_response.get('_serializer') if self.base_response is not None else None

    def __repr__(self):
        return "BookDeleteSerializer=(id={} ......)".format(self.id)


class RepoTocSerializer(BaseSerializer):
    def __init__(self, repo_toc_response: dict):
        super().__init__(repo_toc_response)

    @property
    def repo_toc_response(self) -> Optional[dict]:
        return self.repo_toc_response

    @repo_toc_response.setter
    def repo_toc_response(self, value) -> None:
        self.repo_toc_response = value

    @property
    def title(self) -> Optional[str]:
        return self.base_response.get('title') if self.base_response is not None else None

    @property
    def slug(self) -> Optional[str]:
        return self.base_response.get('slug') if self.base_response is not None else None

    @property
    def depth(self) -> Optional[int]:
        return self.base_response.get('depth') if self.base_response is not None else None

    def __repr__(self):
        return "RepoTocSerializer=(slug={} .....)".format(self.slug)


class DocSerializer(BaseSerializer):
    """
    @See https://www.yuque.com/yuque/developer/docserializer
    """

    def __init__(self, doc_response: dict):
        super().__init__(doc_response)

    @property
    def doc_response(self) -> Optional[dict]:
        return self.base_response

    @doc_response.setter
    def doc_response(self, value: dict) -> None:
        self.base_response = value

    @property
    def id(self) -> Optional[int]:
        return self.doc_response.get("id") if self.doc_response is not None else None

    @property
    def slug(self) -> Optional[str]:
        return self.doc_response.get("slug") if self.doc_response is not None else None

    @property
    def title(self) -> Optional[str]:
        return self.doc_response.get("title") if self.doc_response is not None else None

    @property
    def description(self) -> Optional[str]:
        return self.doc_response.get("description") if self.doc_response is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.doc_response.get("user_id") if self.doc_response is not None else None

    @property
    def book_id(self) -> Optional[int]:
        return self.doc_response.get("book_id") if self.doc_response is not None else None

    @property
    def format(self) -> Optional[str]:
        return self.doc_response.get("format") if self.doc_response is not None else None

    @property
    def public(self) -> Optional[int]:
        return self.doc_response.get("public") if self.doc_response is not None else None

    @property
    def status(self) -> Optional[int]:
        return self.doc_response.get("status") if self.doc_response is not None else None

    @property
    def likes_count(self) -> Optional[int]:
        return self.doc_response.get("comments_count") if self.doc_response is not None else None

    @property
    def comments_count(self) -> Optional[int]:
        return self.doc_response.get("comments_count") if self.doc_response is not None else None

    @property
    def content_updated_at(self) -> Optional[str]:
        return self.doc_response.get("content_updated_at") if self.doc_response is not None else None

    @property
    def created_at(self) -> Optional[str]:
        return self.doc_response.get("created_at") if self.doc_response is not None else None

    @property
    def updated_at(self) -> Optional[str]:
        return self.doc_response.get("updated_at") if self.doc_response is not None else None

    @property
    def published_at(self) -> Optional[str]:
        return self.doc_response.get("published_at") if self.doc_response is not None else None

    @property
    def draft_version(self) -> Optional[int]:
        return self.doc_response.get("draft_version") if self.doc_response is not None else None

    @property
    def last_editor_id(self) -> Optional[int]:
        return self.doc_response.get("last_editor_id") if self.doc_response is not None else None

    @property
    def word_count(self) -> Optional[int]:
        return self.doc_response.get("word_count") if self.doc_response is not None else None

    @property
    def last_editor(self) -> UserSerializer:
        return UserSerializer(
            user_response=self.doc_response.get("last_editor")) if self.doc_response is not None else None

    @property
    def book(self) -> BookSerializer:
        return BookSerializer(
            book_response=self.doc_response.get("book")) if self.doc_response is not None else None

    def __repr__(self):
        return "DocSerializer=(id={!r}) .......".format(self.id)


class DocDetailSerializer(BaseSerializer):
    """
    @See https://www.yuque.com/yuque/developer/docdetailserializer
    """

    def __init__(self, doc_detail_response: dict):
        super().__init__(doc_detail_response)

    @property
    def doc_detail_response(self) -> Optional[dict]:
        return self.doc_detail_response

    @doc_detail_response.setter
    def doc_detail_response(self, value) -> None:
        self.doc_detail_response = value

    @property
    def id(self) -> Optional[int]:
        return self.base_response.get('id') if self.base_response is not None else None

    @property
    def slug(self) -> Optional[str]:
        return self.base_response.get('slug') if self.base_response is not None else None

    @property
    def title(self) -> Optional[str]:
        return self.base_response.get('title') if self.base_response is not None else None

    @property
    def book_id(self) -> Optional[int]:
        return self.base_response.get('book_id') if self.base_response is not None else None

    @property
    def book(self) -> Optional[BookSerializer]:
        return BookSerializer(book_response=self.base_response.get('book')) if self.base_response is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.base_response.get('user_id') if self.base_response is not None else None

    @property
    def creator(self) -> Optional[UserSerializer]:
        return UserSerializer(
            user_response=self.base_response.get('creator')) if self.base_response is not None else None

    @property
    def format(self) -> Optional[str]:
        return self.base_response.get('format') if self.base_response is not None else None

    @property
    def body(self) -> Optional[str]:
        return self.base_response.get('body') if self.base_response is not None else None

    @property
    def body_draft(self) -> Optional[str]:
        return self.base_response.get('body_draft') if self.base_response is not None else None

    @property
    def body_html(self) -> Optional[str]:
        return self.base_response.get('body_html') if self.base_response is not None else None

    @property
    def public(self) -> Optional[int]:
        return self.base_response.get('public') if self.base_response is not None else None

    @property
    def status(self) -> Optional[int]:
        return self.base_response.get('status') if self.base_response is not None else None

    @property
    def likes_count(self) -> Optional[int]:
        return self.base_response.get('likes_count') if self.base_response is not None else None

    @property
    def comments_count(self) -> Optional[int]:
        return self.base_response.get('comments_count') if self.base_response is not None else None

    @property
    def content_updated_at(self) -> Optional[str]:
        return self.base_response.get('content_updated_at') if self.base_response is not None else None

    @property
    def deleted_at(self) -> Optional[str]:
        return self.base_response.get('deleted_at') if self.base_response is not None else None

    @property
    def created_at(self) -> Optional[str]:
        return self.base_response.get('created_at') if self.base_response is not None else None

    @property
    def updated_at(self) -> Optional[str]:
        return self.base_response.get('updated_at') if self.base_response is not None else None

    @property
    def published_at(self) -> Optional[str]:
        return self.base_response.get('published_at') if self.base_response is not None else None

    @property
    def word_count(self) -> Optional[int]:
        return self.base_response.get('word_count') if self.base_response is not None else None

    @property
    def _serializer(self) -> Optional[str]:
        return self.base_response.get('_serializer') if self.base_response is not None else None

    def __repr__(self):
        return "DocDetailSerializer=<id={} .....>".format(self.id)


class GroupUserSerializer(BaseSerializer):
    def __init__(self, group_user_response: dict):
        super().__init__(group_user_response)

    @property
    def group_user_response(self) -> Optional[dict]:
        return self.group_user_response

    @group_user_response.setter
    def group_user_response(self, value) -> None:
        self.group_user_response = value

    @property
    def id(self) -> Optional[int]:
        return self.base_response.get('id') if self.base_response is not None else None

    @property
    def group_id(self) -> Optional[int]:
        return self.base_response.get('group_id') if self.base_response is not None else None

    @property
    def user_id(self) -> Optional[int]:
        return self.base_response.get('user_id') if self.base_response is not None else None

    @property
    def role(self) -> Optional[int]:
        return self.base_response.get('role') if self.base_response is not None else None

    @property
    def created_at(self) -> Optional[str]:
        return self.base_response.get('created_at') if self.base_response is not None else None

    @property
    def updated_at(self) -> Optional[str]:
        return self.base_response.get('updated_at') if self.base_response is not None else None

    @property
    def user(self) -> Optional[UserSerializer]:
        return UserSerializer(user_response=self.base_response.get('user')) if self.base_response is not None else None

    def __repr__(self):
        return "GroupUserSerializer=<{} ......>".format(self.id)


class DocSerializerList(BaseSerializer):
    def __init__(self, base_response: dict) -> None:
        super().__init__(base_response)

    @property
    def doc_serializer_list(self) -> List[DocSerializer]:
        return [DocSerializer(doc_response=doc) for doc in
                self.base_response] if self.base_response is not None else []


class BookSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def book_serializer_list(self) -> List[BookSerializer]:
        return [BookSerializer(book) for book in
                self.base_response] if self.base_response is not None else []


class UserSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def user_serializer_list(self) -> List[UserSerializer]:
        return [UserSerializer(user_response=user) for user in
                self.base_response] if self.base_response is not None else []


class RepoTocSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def repo_toc_serializer_list(self) -> List[RepoTocSerializer]:
        return [RepoTocSerializer(repo_toc_response=rt_response) for rt_response in
                self.base_response] if self.base_response is not None else []


class DocDetailSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def doc_detail_serializer_list(self) -> Optional[DocDetailSerializer]:
        return [DocDetailSerializer(doc_detail_response=doc) for doc in
                self.base_response] if self.base_response is not None else None


class GroupUserSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def group_user_serializer_list(self) -> Optional[DocDetailSerializer]:
        return [GroupUserSerializer(group_user_response=doc) for doc in
                self.base_response] if self.base_response is not None else None


# Quick
class QuickDocStructure(object):
    def __init__(self, doc_serializer: DocSerializer = None, doc_detail_serializer: DocDetailSerializer = None):
        self._doc_serializer = doc_serializer
        self._doc_detail_serializer = doc_detail_serializer

    @property
    def doc_detail_serializer(self):
        return self._doc_detail_serializer

    @doc_detail_serializer.setter
    def doc_detail_serializer(self, doc_detail_serializer):
        self._doc_detail_serializer = doc_detail_serializer

    @property
    def doc_serializer(self):
        return self._doc_serializer

    @doc_serializer.setter
    def doc_serializer(self, doc_serializer):
        self._doc_serializer = doc_serializer


class QuickRepoStructure(object):
    def __init__(self,
                 quick_doc_structure_list: List[QuickDocStructure] = None,
                 repo_serializer: BookSerializer = None,
                 repo_detail_serializer: BookDetailSerializer = None):
        self._quick_doc_structure_list = quick_doc_structure_list or []
        self._repo_serializer = repo_serializer
        self._repo_detail_serializer = repo_detail_serializer

    # Doc List
    @property
    def quick_doc_structure_list(self):
        return self._quick_doc_structure_list

    @quick_doc_structure_list.setter
    def quick_doc_structure_list(self, quick_doc_structure_list):
        self._quick_doc_structure_list = quick_doc_structure_list

    def add_quick_doc_structure(self, quick_doc_structure):
        self._quick_doc_structure_list.append(quick_doc_structure)

    # Repo Detail
    @property
    def repo_detail_serializer(self):
        return self._repo_detail_serializer

    @repo_detail_serializer.setter
    def repo_detail_serializer(self, repo_detail_serializer):
        self._repo_detail_serializer = repo_detail_serializer

    # Repo Basic
    @property
    def repo_serializer(self):
        return self._repo_serializer

    @repo_serializer.setter
    def repo_serializer(self, repo_serializer):
        self._repo_serializer = repo_serializer


class QuickGroupStructure(object):
    def __init__(self,
                 quick_repo_structure_list: QuickRepoStructure = None,
                 group_user_serializer: GroupUserSerializer = None):
        self._quick_repo_structure_list = quick_repo_structure_list or []
        self._group_user_serializer = group_user_serializer

    @property
    def group_user_serializer(self):
        return self._group_user_serializer

    @group_user_serializer.setter
    def group_user_serializer(self, group_user_serializer):
        self._group_user_serializer = group_user_serializer

    @property
    def quick_repo_structure_list(self):
        return self._quick_repo_structure_list

    @quick_repo_structure_list.setter
    def quick_repo_structure_list(self, quick_repo_structure_list):
        self._quick_repo_structure_list = quick_repo_structure_list


class QuickUserStructure(object):
    def __init__(self,
                 quick_group_structure_list: List[QuickGroupStructure] = None,
                 quick_repo_structure_list: List[QuickRepoStructure] = None,
                 user_serializer: UserSerializer = None):
        self._quick_group_structure_list = quick_group_structure_list or []
        self._quick_repo_structure_list = quick_repo_structure_list or []
        self._user_serializer = user_serializer or None

    # Group
    @property
    def quick_group_structure_list(self) -> List[QuickGroupStructure]:
        return self._quick_group_structure_list

    @quick_group_structure_list.setter
    def quick_group_structure_list(self, quick_group_structure_list):
        self._quick_group_structure_list = quick_group_structure_list

    # Repo
    @property
    def quick_repo_structure_list(self) -> List[QuickRepoStructure]:
        return self._quick_repo_structure_list

    @quick_repo_structure_list.setter
    def quick_repo_structure_list(self, quick_repo_structure_list):
        self._quick_repo_structure_list = quick_repo_structure_list

    # User
    @property
    def user_serializer(self):
        return self._user_serializer

    @user_serializer.setter
    def user_serializer(self, user_serializer):
        self._user_serializer = user_serializer
