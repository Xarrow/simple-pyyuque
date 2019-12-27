# -*- coding:utf-8 -*-
from simple_pyyuque_utils import *


class PersistentCallbackBase(object):
    def __init__(self, persistent_path: str, token_map: dict = None):
        """
        :param persistent_path:         Token  持久化位置
        :param token_map:               Token Map
        """
        self._persistent_path = persistent_path
        self._local_persistent_path = None
        self._token_map = token_map

    @property
    def local_persistent_path(self):
        return self._local_persistent_path

    @property
    def token_map(self):
        return self._token_map

    def _is_prepared_local_fetch(self, default_file_name: str):
        """
        读取本地文件准备
        """
        # 完整授权文件不存在
        tmp = None
        if self._local_persistent_path is None:
            if os.path.isdir(self._persistent_path):
                ll = os.listdir(self._persistent_path)
                if len(ll) < 1:
                    raise PersistentCallbackBaseException(
                        "PersistentCallbackBase fetch  token failed, {0} is blank".format(self._persistent_path))
                if len(ll) > 0:
                    for i in ll:
                        if i.endswith(default_file_name):
                            tmp = os.path.join(self._persistent_path, i)

                if is_blank(tmp):
                    raise PersistentCallbackBaseException(
                        "PersistentCallbackBase fetch  token failed, {0} can not found in {1}".format(
                            default_file_name, self._persistent_path))

            elif os.path.isfile(self._persistent_path):
                tmp = self._persistent_path
            else:
                raise PersistentCallbackBaseException(
                    "PersistentCallbackBase fetch  token failed, unknown file")
        else:
            tmp = self._local_persistent_path
        self._local_persistent_path = tmp

    def _is_prepared_local_persistent(self, default_file_name: str):
        """
        为持久化本地文件做做准备
        :return:
        """
        # 获取 token 失败
        if is_blank(self._token_map):
            raise PersistentCallbackBaseException("PersistentCallbackBase persistent  token failed, token_map is blank")
        if self._token_map.get('access_token') is None:
            raise PersistentCallbackBaseException(
                "PersistentCallbackBase persistent  token failed, token_map is invalid")
        is_file = True
        try:
            # dir
            if self._persistent_path.endswith("/") or os.path.isdir(self._persistent_path):
                is_file = False
                if not os.path.isdir(self._persistent_path):
                    os.makedirs(self._persistent_path)
            # file
            else:
                dir_path = os.path.dirname(self._persistent_path)
                if not os.path.isdir(os.path.abspath(dir_path)):
                    os.makedirs(dir_path)

            tmp = self._persistent_path
            if not is_file:
                tmp = os.path.join(self._persistent_path, default_file_name)
            self._local_persistent_path = tmp
        except Exception as ex:
            raise PersistentCallbackBaseException("Persistent pickle token exception, {0}".format(ex))

    def do_persistent(self):
        raise Exception("not implement")

    def do_fetch(self):
        raise Exception("not implement")


class BaseAuth(object):
    def __init__(self):
        self._auth_valid: bool = False

    def get_token_map(self):
        raise Exception("not implement")

    def get_cookies_map(self):
        raise Exception("not implement")
