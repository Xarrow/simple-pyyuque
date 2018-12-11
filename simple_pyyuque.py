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


import logging
import sys
import asyncio
import requests
from typing import Optional, Union, List
from enum import Enum

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

PY3_7 = False

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 5
    PY3_7 = True if sys.version_info.minor == 7 else PY3_7

except Exception as ex:
    raise AssertionError("simple-pyyuque only support 3.6+.")

IS_DEBUG = logger.level == logging.DEBUG
BASIC_URL = 'https://www.yuque.com/api/v2/'
MESSAGE_TEMPLATE_A = """# {method_name} , `{p1}` and `{p2}` can not both be blank ! For further API detail please 
visit `{doc_uri}` """
MESSAGE_TEMPLATE_B = """# {method_name} , `{p1}` is not blank ! For further API detail please visit `{doc_uri}` """


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
    DATA_NOT_REALASE = {"code": 404, "message": "数据不存在，或未开放", }
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


class YuQueAPIException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class BaseSerializer(object):
    __slots__ = ['_base_response']

    def __init__(self, base_response: dict):
        self._base_response = base_response

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
    def name(self):
        return self.user_response.get('name') if self.user_response is not None else None

    @property
    def description(self):
        return self.user_response.get('description') if self.user_response is not None else None

    @property
    def avatar_url(self):
        return self.user_response.get('avatar_url') if self.user_response is not None else None

    @property
    def created_at(self):
        return self.user_response.get('created_at') if self.user_response is not None else None

    @property
    def updated_at(self):
        return self.user_response.get('updated_at') if self.user_response is not None else None

    def __repr__(self):
        return 'UserSerializer=(id={!r},type={!r},{!r})description={!r},acatar_url={!r},created_at={!r},upadate_at={' \
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
        return self.base_response.get("slug ") if self.base_response is not None else None

    # name - 名称
    @property
    def name(self) -> Optional[int]:
        return self.base_response.get("name") if self.base_response is not None else None

    # namespace - 仓库完整路径 user.login/book.slug
    @property
    def namespace(self) -> Optional[str]:
        return self.base_response.get("namespace ") if self.base_response is not None else None

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
        return self.base_response.get("creator_id ") if self.base_response is not None else None

    # public - 公开状态 [1 - 公开, 0 - 私密]
    @property
    def public(self) -> Optional[int]:
        return self.base_response.get("public") if self.base_response is not None else None

    # likes_count - 喜欢数量
    @property
    def likes_count(self) -> Optional[int]:
        return self.base_response.get("likes_count ") if self.base_response is not None else None

    # watches_count - 订阅数量
    @property
    def watches_count(self) -> Optional[int]:
        return self.base_response.get("watches_count ") if self.base_response is not None else None

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
        return "DocDetailSerializer=<{} .....>".format(self.id)


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
    def doc_serializer_list(self) -> Optional[List[UserSerializer]]:
        return [DocSerializer(doc_response=doc) for doc in
                self.base_response] if self.base_response is not None else None


class BookSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def book_serializer_list(self) -> Optional[List[BookSerializer]]:
        return [BaseSerializer(base_response=book) for book in
                self.base_response] if self.base_response is not None else None


class UserSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def user_serializer_list(self) -> Optional[List[UserSerializer]]:
        return [UserSerializer(user_response=user) for user in
                self.base_response] if self.base_response is not None else None


class RepoTocSerializerList(BaseSerializer):
    def __init__(self, base_response: dict):
        super().__init__(base_response)

    @property
    def repo_toc_serializer_list(self) -> Optional[List[RepoTocSerializer]]:
        return [RepoTocSerializer(repo_toc_response=rt_response) for rt_response in
                self.base_response] if self.base_response is not None else None


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


class BaseAPI(object):
    __slots__ = ['_session', '_loop', '_token', '_app_name', '_headers']

    def __init__(self, token: str, app_name: str, **kwargs):
        assert is_not_blank(value=token)
        self._session = requests.Session()
        self._loop = asyncio.get_event_loop()
        self._token = token
        self._app_name = app_name or 'py_simple_yuque'
        self._headers = {
            'User-agent': self._app_name,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Auth-Token': self._token
        }

    def _api_request(self, method: object, source_name: str, **kwargs) -> Optional[dict]:
        if isinstance(method, str):
            kwargs['method'] = method
        elif isinstance(method, RequestMethods):
            kwargs['method'] = method.value

        kwargs['url'] = BASIC_URL + \
                        (source_name if not source_name.startswith("/") else source_name[1:len(source_name)])
        kwargs['headers'] = self._headers

        async def _inner_request():
            async def _a():
                return self._session.request(**kwargs)

            return await _a()

        res = self._loop.run_until_complete(_inner_request())
        sc = res.status_code
        if sc != 200:
            message = "#api_request , request failed , kwargs=%s , messages=%s - %s  , result=%s" % (
                kwargs, sc, STATUS_CODE_MAPPING.get(sc), res.text)
            raise YuQueAPIException(message)
        return res.json().get("data") if is_not_blank(res.json().get('data')) else None

    def get_request(self, source_name: str, res_type, **kwargs) -> Optional[Union[dict, BaseSerializer]]:
        res = self._api_request(method=RequestMethods.GET, source_name=source_name, **kwargs)
        if res_type is not None:
            return None if res is None else res_type(res)
        return res

    def post_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.POST, source_name=source_name, **kwargs)
        if res_type is not None:
            return None if res is None else res_type(res)
        return res

    def put_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.PUT, source_name=source_name, **kwargs)
        if res_type is not None:
            return None if res is None else res_type(res)
        return res

    def delete_request(self, source_name: str, res_type, **kwargs) -> Optional[BaseSerializer]:
        res = self._api_request(method=RequestMethods.DELETE, source_name=source_name, **kwargs)
        if res_type is not None:
            return None if res is None else res_type(res)
        return res

    def head_request(self, source_name: str, res_type, **kwargs) -> Optional[dict]:
        res = self._api_request(method=RequestMethods.HEAD, source_name=source_name, **kwargs)
        if res_type is not None:
            return None if res is None else res_type(res)
        return res


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
        if hasattr(BaseRelation.yuque_api, "fdel"):
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

    class Group(BaseRelation):
        # Group - 组织
        # @See https://www.yuque.com/yuque/developer/group
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
            :param login:           login
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
            :return:
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

    class Repo(BaseRelation):

        # Repo - 仓库
        # @See https://www.yuque.com/yuque/developer/rep
        def get_users_repos(self,
                            type: Union[RepoType, str] = RepoType.ALL,
                            include_membered: bool = False,
                            offset: int = 1,
                            login: str = None,
                            id: int = None) -> Optional[BookSerializerList]:
            """
            获取某个用户的仓库列表
            GET /users/:login/repos
            GET /users/:id/repos
            :param type:                Book, Design, all - 所有类型
            :param include_membered:    true 包含用户参加的仓库，false 只返回用户创建的
            :param offset:              用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :param login:
            :param id:
            :return:                     Optional[BookSerializerList]
            """
            if is_blank(login) and is_blank(id):
                # TODO
                pass
            params = {"type": type.value if isinstance(type, RepoType) else type, "include_membered": include_membered,
                      "offset": offset}
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
            获取某个组织的仓库列表
            GET /groups/:login/repos
            GET /groups/:id/repos

            :param type:                Book, Design, all - 所有类型
            :param include_membered:    true 包含用户参加的仓库，false 只返回用户创建的
            :param offset:              用于分页，效果类似 MySQL 的 limit offset，一页 20 条
            :param login:
            :param id:
            :return:                     Optional[BookSerializerList]
            """
            if is_blank(login) and is_blank(id):
                # TODO
                pass
            return self.get_users_repos(type=type, include_membered=include_membered, offset=offset, login=login, id=id)

        def post_users_repos(self, name: str,
                             slug: str,
                             description: str = "",
                             public: Union[RepoPublic, int] = RepoPublic.PRIVATE,
                             type: Union[RepoType, str] = RepoType.BOOK,
                             login: str = None, id: int = None) -> Optional[BookSerializer]:
            """
            创建新仓库
            往自己下面创建仓库
            POST /users/:login/repos
            POST /users/:id/repos

            :param name:            仓库名称
            :param slug:            slug
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param type:            ‘Book’ 文库, ‘Design’ 画板, 请注意大小写
            :param login:
            :param id:
            :return:                 Optional[BookSerializer]
            """
            if is_blank(login) and is_blank(id):
                # TODO
                pass

            if is_blank(name):
                pass
            if is_blank(slug):
                pass

            data = {"name": name, "slug": slug, "description": description, "public": public.value, "type": type.value}
            return self.yuque_api.post_request(
                source_name="/groups/{}/repos".format(login if is_not_blank(login) else id),
                res_type=BookSerializer, data=data)
            pass

        def post_groups_repos(self, name: str,
                              slug: str,
                              description: str = "",
                              public: Union[RepoPublic, int] = RepoPublic.PRIVATE,
                              type: Union[RepoType, str] = RepoType.BOOK,
                              login: str = None, id: int = None) -> Optional[BookSerializer]:
            """
            创建新仓库
            往组织创建仓库
            POST /groups/:login/repos
            POST /groups/:id/repos
            :param name:            仓库名称
            :param slug:            slug
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param type:            ‘Book’ 文库, ‘Design’ 画板, 请注意大小写
            :param login:
            :param id:
            :return:                 Optional[BookSerializer]
            """
            if is_blank(login) and is_blank(id):
                # TODO
                pass

            if is_blank(name):
                pass
            if is_blank(slug):
                pass

            return self.post_users_repos(name=name, slug=slug, description=description, public=public, type=type,
                                         login=login, id=id)

        def get_repos(self,
                      namespace: str = None,
                      id: int = None,
                      type: Union[str, RepoType] = RepoType.BOOK) -> \
                Optional[BookDetailSerializer]:
            """
            获取仓库详情
            GET /repos/:namespace
            # 或
            GET /repos/:id
            :param namespace:
            :param id:
            :param type:        仓库类型，Book - 文库，Design - 设计稿
            :return:            Optional[BookDetailSerializer]
            """
            if is_blank(namespace) and is_blank(id):
                # TODO
                pass
            params = {"type": type.value if isinstance(type, RepoType) else type}
            return self.yuque_api.get_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDetailSerializer,
                params=params)

        def put_repos(self,
                      name: str,
                      slug: str,
                      toc: str,
                      description: str = "",
                      public: Union[int, RepoPublic] = RepoPublic.PRIVATE,
                      namespace: str = None, id: int = None, ) -> Optional[BookDetailSerializer]:

            """
            更新仓库信息

            :param name:            仓库名称
            :param slug:             slug
            :param toc:             更新文档仓库的目录信息
            :param description:     说明
            :param public:          0 私密, 1 内网公开, 2 全网公开
            :param namespace:
            :param id:
            :return:                 Optional[BookDetailSerializer]
            """
            if is_blank(namespace) and is_blank(id):
                pass

            if is_blank(name):
                pass
            if is_blank(slug):
                pass
            data = {"name": name, "slug": slug, "toc": toc, "description": description,
                    "public": public.value if isinstance(public, RepoPublic) else public}

            return self.yuque_api.put_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDetailSerializer,
                data=data)

        def delete_repo(self, namespace: str = None, id: int = None) -> Optional[BookDeleteSerializer]:
            """
            删除仓库
            DELETE /repos/:namespace
            # 或
            DELETE /repos/:id
            :param namespace:
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(id):
                pass
            return self.yuque_api.delete_request(
                source_name="/repos/{}".format(namespace if is_not_blank(namespace) else id),
                res_type=BookDeleteSerializer)

        def repos_toc(self, namespace: str = None, id: int = None) -> Optional[RepoTocSerializerList]:
            """
            获取一个仓库的目录结构
            GET /repos/:namespace/toc
            # 或
            GET /repos/:id/toc

            :param namespace:
            :param id:
            :return:
            """
            if is_blank(namespace) and is_blank(id):
                pass
            return self.yuque_api.get_request(
                source_name="/repos/{}/toc".format(namespace if is_not_blank(namespace) else id),
                res_type=RepoTocSerializerList)

        def search_repos(self, q: str, type: Union[str, RepoType] = RepoType.BOOK) -> Optional[BookSerializerList]:
            """
            基于关键字搜索仓库
            GET /search/repos?q=&type=
            :param q:       关键字，目前是简单的数据库模糊查询
            :param type:    类型 (Book, Design），注意大小写，不传搜索所有类型
            :return:        Optional[BookSerializerList]
            """
            if is_blank(q):
                pass
            params = {"q": q, "type": type.value if isinstance(type, RepoType) else type}
            return self.yuque_api.get_request(source_name="/search/repos", res_type=BookSerializerList, params=params)

        def get_repo(self, **kwargs) -> Optional[BookSerializerList]:
            """
            获取用户或者企业仓库
            :param kwargs:
            :return:
            """
            return self.get_users_repos(**kwargs)

        def get_repos_detail(self, **kwargs) -> Optional[BookDetailSerializer]:
            """
            获取仓库详情
            :param kwargs:
            :return:
            """
            return self.get_repos(**kwargs)

        def create_repos(self, **kwargs) -> Optional[BookSerializer]:
            """
            创建仓库
            :param kwargs:
            :return:
            """
            return self.post_users_repos(**kwargs)

        def update_repos(self, **kwargs) -> Optional[BookDetailSerializer]:
            """
            更新仓库
            :param kwargs:
            :return:
            """
            return self.put_repos(**kwargs)

    class Doc(BaseRelation):

        # ==> Doc
        # @See https://www.yuque.com/yuque/developer/doc
        def get_repos_docs(self,
                           namespace: str = None,
                           id: int = None) -> Optional[DocSerializerList]:
            if is_blank(namespace) and is_blank(id):
                raise YuQueAPIException("#repo_docs , namespace and id can not both be blank !")
            return self.yuque_api.get_request(
                source_name="/repos/{}/docs".format(namespace if is_not_blank(namespace) else id),
                res_type=DocSerializerList)

        def get_docs(self, **kwargs) -> Optional[DocSerializerList]:
            return self.get_repos_docs(**kwargs)

        def get_repos_docs_detail(self, namespace: str = None, slug: str = None, repo_id: str = None, id: int = None,
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
            if is_blank(namespace) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_docs_detail",
                                                    p1="namespace", p2="repo_id",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            if is_not_blank(namespace) and is_blank(slug):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_docs_detail",
                                                    p1="namespace", p2="slug",
                                                    doc_uri="https://www.yuque.com/yuque/developer/doc")
                raise YuQueAPIException(message)

            if is_not_blank(repo_id) and is_blank(id):
                message = MESSAGE_TEMPLATE_A.format(method_name="repos_docs_detail",
                                                    p1="repo_id", p2="id",
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
                           repo_id: str = None,
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

        def delete_repos_docs(self, namespace: str = None,
                              repo_id: str = None,
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
