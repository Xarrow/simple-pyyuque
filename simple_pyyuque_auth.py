# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_oauth.py
 Time: 2019/12/23
"""
import base64
import hashlib
import hmac
import json
import pickle
import time
import webbrowser
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver import ChromeOptions

import requests

from simple_pyyuque_base import PersistentCallbackBase, BaseAuth
from simple_pyyuque_utils import *


class JsonPersistentCallback(PersistentCallbackBase):
    """
    JSON Token
    """

    def do_persistent(self):
        try:
            self._is_prepared_local_persistent(default_file_name="token.json")
        except PersistentCallbackBaseException as ex:
            raise ex
        with open(self._local_persistent_path, mode='w') as fd:
            json.dump(self._token_map, fd)
        return self

    def do_fetch(self):
        try:
            self._is_prepared_local_fetch(default_file_name="token.json")
        except PersistentCallbackBaseException as ex:
            raise ex
        with open(self._local_persistent_path, mode="r") as fd:
            _tmp_token_map = json.load(fd, encoding='utf-8')
            self._token_map = _tmp_token_map
        return self


class PicklePersistentCallback(PersistentCallbackBase):
    """
    Pickle Token 持久化
    """

    def do_persistent(self):
        try:
            self._is_prepared_local_persistent(default_file_name="token.pickle")
        except PersistentCallbackBaseException as ex:
            raise ex
        with open(self._local_persistent_path, mode='wb') as fd:
            pickle.dump(self._token_map, fd)
        return self

    def do_fetch(self):
        try:
            self._is_prepared_local_fetch(default_file_name="token.pickle")
        except PersistentCallbackBaseException as ex:
            raise ex
        with open(self._local_persistent_path, mode="rb") as fd:
            _tmp_token_map = pickle.load(fd, encoding='utf-8')
            self._token_map = _tmp_token_map
        return self


class SimpleYuQueSimulateLoginOption(object):
    def __init__(self,
                 username: str = None,
                 password: str = None,
                 chrome_options: ChromeOptions = None,
                 webdriver_execute_path: str = None,
                 need_download_webdrive: bool = False,
                 is_debug: bool = False):
        self._username = username
        self._password = password
        self._chrome_options = chrome_options or ChromeOptions()
        self._webdriver_execute_path = webdriver_execute_path
        self._is_debug: bool = is_debug
        self._need_download_webdrive = need_download_webdrive

    def prepare_options(self):
        # download webdriver
        # if self._webdriver_execute_path is None and self._need_download_webdrive:
        #     default_webdrive_path = "webdriver"
        #     if os.path.isdir(default_webdrive_path):
        #         default_webdrive_files = os.listdir(default_webdrive_path)
        #         if len(default_webdrive_files) > 0:
        #             default_webdrive_execute_file = os.path.join(default_webdrive_path, default_webdrive_files[0])
        #             if os.path.isfile(default_webdrive_execute_file):
        #                 print("==> webdriver has exist at {0}".format(default_webdrive_execute_file))
        #                 self._webdriver_execute_path = default_webdrive_execute_file
        #
        #     if self._webdriver_execute_path is None:
        #         if WINDOWS:
        #             os_name = "Windows"
        #             webdriver_download_url = "http://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_win32.zip"
        #         elif DARWIN:
        #             os_name = "Mac OS"
        #             webdriver_download_url = "http://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_mac64.zip"
        #         elif LINUX:
        #             os_name = "Linux"
        #             webdriver_download_url = "http://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip"
        #         else:
        #             raise Exception("SimpleYuQueSimulateLoginOptions, unknown platform !")
        #         print("==> current operation system : {0}".format(os_name))
        #         print("==> prepare download webdriver : {0}".format(webdriver_download_url))
        #         default_download_tmp = "tmp"
        #         webdriver_zip_filename = webdriver_download_url.split("/")[-1]
        #         webdriver_local_zip_filepath = os.path.join(default_download_tmp, webdriver_zip_filename)
        #
        #         # not exist
        #         if not os.path.isfile(webdriver_local_zip_filepath):
        #             # http = SOCKSProxyManager('socks5://localhost:1086/')
        #             http = PoolManager()
        #             response = http.request('GET', webdriver_download_url, preload_content=False)
        #             if not os.path.isdir(default_download_tmp):
        #                 os.mkdir(default_download_tmp)
        #             with open(webdriver_local_zip_filepath, mode="wb") as fd:
        #                 while True:
        #                     data = response.read(1024)
        #                     if not data:
        #                         break
        #                     fd.write(data)
        #             response.release_conn()
        #             print("==> webdriver zip file download finished , location at : {0}".format(
        #                 os.path.abspath(webdriver_local_zip_filepath)))
        #         else:
        #             print("==> webdriver zip file has existed at {0}".format(webdriver_local_zip_filepath))
        #         with ZipFile(webdriver_local_zip_filepath, 'r') as zipfile:
        #             zipfile.extractall(path=default_webdrive_path)
        #
        #         self._webdriver_execute_path = os.path.join(default_webdrive_path, os.listdir(default_webdrive_path)[0])

        if is_blank(self._webdriver_execute_path):
            raise Exception("SimpleYuQueSimulateLoginOption , webdriver_execute_path is blank!")
        if not os.path.isfile(self._webdriver_execute_path):
            raise Exception("SimpleYuQueSimulateLoginOption , webdriver_execute_path is not exist, this is file!")

        if LINUX or DARWIN:
            os.chmod(self._webdriver_execute_path, 0o777)

        self._chrome_options.add_argument('--no-sandbox')
        self._chrome_options.add_argument('--disable-dev-shm-usage')
        self._chrome_options.add_argument('--disable-gpu')
        self._chrome_options.add_argument("--disable-dev-shm-usage")
        self._chrome_options.add_argument("start-maximized")
        self._chrome_options.add_argument("disable-infobars")
        self._chrome_options.add_argument("--disable-extensions")
        if not self._is_debug:
            self._chrome_options.add_argument("--headless")
        if self._is_debug:
            print("SimpleYuQueSimulateLoginOptions:")
            print("==> webdriver_execute_path:{0}".format(os.path.abspath(self._webdriver_execute_path)))

        return self

    # def _auto_adapt_webdriver(self):
    #     # https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#requirements
    #
    #     WEBDRIVER_DOWNLOAD_VERSION_MAPPING = {
    #         "70": 'http://chromedriver.storage.googleapis.com/70.0.3538.97/',
    #         "71": 'http://chromedriver.storage.googleapis.com/71.0.3578.80/',
    #         '72': 'http://chromedriver.storage.googleapis.com/72.0.3626.7/',
    #         '73': 'http://chromedriver.storage.googleapis.com/73.0.3683.68/',
    #         '74': 'http://chromedriver.storage.googleapis.com/74.0.3729.6/',
    #         '75': 'http://chromedriver.storage.googleapis.com/75.0.3770.90/',
    #         '76': 'http://chromedriver.storage.googleapis.com/76.0.3809.68/',
    #         '77': 'http://chromedriver.storage.googleapis.com/77.0.3865.40/',
    #         '78': 'http://chromedriver.storage.googleapis.com/78.0.3904.70/',
    #         '79': 'http://chromedriver.storage.googleapis.com/79.0.3945.36/',
    #         'latest': ''
    #     }
    #     import subprocess
    #     try:
    #
    #         DEFAULT_LINUX_GOOGLE_CHROME_LOCATION = '/usr/bin/google-chrome'
    #         with subprocess.Popen(args=[DEFAULT_LINUX_GOOGLE_CHROME_LOCATION, '--version'],
    #                               stdout=subprocess.PIPE) as sub:
    #             google_chrome_version = str(sub.communicate()[0])
    #             print("==> current google-chrome version is {0}".format(google_chrome_version))
    #             major_version = google_chrome_version.split(" ")[2].split('.')[0]
    #             print(major_version)
    #     except Exception as ex:
    #         print("==> current os do not install google-chrome")
    #         print("==> starting install google-chrome")
    #         centos_cmd = """
    #         """
    #         # with subprocess.Popen([centos_cmd], stdout=subprocess.PIPE) as proc:
    #         #     print(proc.communicate())
    #
    #     pass

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def chrome_options(self) -> ChromeOptions:
        return self._chrome_options

    def set_chrome_options(self, chrome_options: ChromeOptions):
        self._chrome_options = chrome_options
        return self

    @property
    def webdriver_execute_path(self) -> str:
        return self._webdriver_execute_path

    def set_webdriver_execute_path(self, webdriver_execute_path: str):
        self._webdriver_execute_path = webdriver_execute_path
        return self

    @property
    def need_download_webdrive(self):
        return self._need_download_webdrive

    def set_need_download_webdrive(self, need_download_webdrive: bool):
        self._need_download_webdrive = need_download_webdrive
        return self

    @property
    def is_debug(self):
        return self._is_debug

    def set_debug(self, is_debug: bool):
        self._is_debug = is_debug
        return self


# TODO
class SimpleYuQueOAuth4Web(BaseAuth):
    pass


class SimpleYuQueSimulateLogin(BaseAuth):
    def __init__(self, options: SimpleYuQueSimulateLoginOption):
        super().__init__()
        self._options = options
        self._cookies = None

    def express(self):
        browser = webdriver.Chrome(executable_path=self._options.webdriver_execute_path,
                                   chrome_options=self._options.chrome_options)
        try:
            browser.get("https://www.yuque.com/login")
            browser.find_element_by_xpath("//input[@data-testid='prefix-phone-input']").send_keys(
                self._options.username)
            browser.find_element_by_xpath("//input[@data-testid='loginPasswordInput']").send_keys(
                self._options.password)
            browser.find_element_by_xpath("//button[@data-testid='btnLogin']").click()
            time.sleep(3)
            browser.get(url="https://www.yuque.com/dashboard")
            if 'loginPasswordInput' in browser.page_source:
                print("login failed")
            print("login success")
            self._auth_valid = True
            print(browser.get_cookies())
        except Exception as ex:
            print(ex)
        finally:
            browser.close()


class SimpleYuQueOAuth4Server(BaseAuth):
    # https://www.yuque.com/yuque/developer/authorizing-oauth-apps#Z8ye5
    def __init__(self, client_id: Union[str, bytes] = None, secret_id: Union[str, bytes] = None,
                 scope: str = "doc,repo,group,topic", open_in_console: bool = True,
                 persistent_path: str = os.path.curdir, persistent_callback=PicklePersistentCallback,
                 is_raise: bool = False):

        super().__init__()
        self._client_id = client_id
        self._secret_id = secret_id
        self._scope = scope
        self._open_in_console = open_in_console
        self._auth_map = {"client_id": self._client_id if isinstance(self._client_id, str) else str(self._client_id,
                                                                                                    encoding='utf-8'),
                          "code": generate_random_code(),
                          "response_type": "code",
                          "scope": self._scope,
                          "timestamp": str(int(time.time() * 1000))}
        self._auth_url = ""
        self._auth_code = ""
        self._token_map = None
        self._persistent_path = persistent_path
        self._persistent_callback = persistent_callback
        self._persistent_callback_instance = None
        self._is_raise = is_raise

    def _sign(self):
        message = bytes(urlencode(query=self._auth_map, encoding='utf-8'), encoding='utf-8')
        dig = hmac.new(
            key=self._secret_id if isinstance(self._secret_id, bytes) else bytes(self._secret_id, encoding='utf-8'),
            msg=message,
            digestmod=hashlib.sha1).digest()
        sign = base64.b64encode(dig).decode()
        self._auth_map['sign'] = sign
        return self

    def _auth_urlencode(self):
        self._auth_url = '{0}?{1}'.format(YUQUE_OAUTH_AUTHORIZE_URL, urlencode(self._auth_map))
        return self

    def _wait_for_auth_code(self):
        if self._open_in_console:
            print("Please copy url {0} in browser and paste code in shell.".format(self._auth_url))
        else:
            try:
                webbrowser.open(url=self._auth_url)
            except Exception as ex:
                print("Your Platform can not support webbrowser.")
                raise ex
        self._auth_code = input("Please enter your code:")
        return self

    def _exchange_token(self):
        exchange_data = {
            "client_id": self._client_id if isinstance(self._client_id, str) else str(self._client_id,
                                                                                      encoding='utf-8'),
            "code": self._auth_code,
            "grant_type": "client_code"
        }
        res = requests.post(url=YUQUE_OAUTH_EXCHANGE_TOKEN_URL, data=exchange_data)
        self._token_map = res.json()
        return self

    def _persistent_token(self):
        try:
            persistent_callback_instance = self._persistent_callback(persistent_path=self._persistent_path,
                                                                     token_map=self._token_map)

            persistent_callback_instance.do_persistent()
            self._persistent_callback_instance = persistent_callback_instance
        except PersistentCallbackBaseException as ex:
            if self._is_raise:
                raise ex
        return self

    def _fetch_token(self):
        try:
            if self._token_map is None:
                if self._persistent_callback_instance is not None:
                    self._token_map = self._persistent_callback_instance.do_fetch().token_map
                    return self
                else:
                    self._persistent_callback_instance = self._persistent_callback(
                        persistent_path=self._persistent_path)
                    self._token_map = self._persistent_callback_instance.do_fetch().token_map
                    return self
        except PersistentCallbackBaseException as ex:
            if self._is_raise:
                raise ex
        return self

    def get_token(self):
        #  内存中存在
        if is_not_blank(self._token_map):
            return self._token_map
        # 持久化文件中存在
        if is_not_blank(self._persistent_path):
            _tmp_token = self._fetch_token()._token_map
            if _tmp_token is not None:
                self._token_map = _tmp_token
                return _tmp_token
        # 重新验证
        try:
            self._sign()
            self._auth_urlencode()
            self._wait_for_auth_code()
            self._exchange_token()
            self._persistent_token()
        except Exception as ex:
            print(ex)
        return self._token_map
