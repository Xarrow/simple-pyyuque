# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: simple_pyyuque_oauth.py
 Time: 2019/12/23
"""
import requests
from abc import abstractmethod, ABC
from http.server import BaseHTTPRequestHandler, HTTPServer
from simple_pyyuque_utils import logger, is_blank, is_not_blank
from urllib3.util import parse_url

# https://www.yuque.com/oauth2/authorize?client_id=TSJjgMa1QIj5acgAHcvF&scope=doc,repo,group:read&redirect_uri=http://localhost:7777/yuqueCallback&state=2&response_type=code
YUQUE_OAUTH_AUTHORIZE_URL = "https://www.yuque.com/oauth2/authorize"
YUQUE_OAUTH_EXCHANGE_TOKEN_URL = 'https://www.yuque.com/oauth2/token'


class _EmbedServer(BaseHTTPRequestHandler, ABC):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logger.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        _query = parse_url(url=self.path).query

        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if is_not_blank(_query):
            items = str(_query).split("&")
            code = None
            state = None
            for i in items:
                key = i.split("=")[0]
                value = i.split("=")[1]
                if key == 'code':
                    code = value
                if key == 'state':
                    state = value
            if is_not_blank(code) and is_not_blank(state):
                self.exchange_token(code, state)

    @abstractmethod
    def exchange_token(self, code, state: str = None):
        print(code,state)
        pass

    @classmethod
    def run(cls, port=7777):
        server_address = ('', port)
        httpd = HTTPServer(server_address, cls)
        logger.info('Starting httpd...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logger.info('Stopping httpd...\n')


class SimpleYuQueOAuth(_EmbedServer):
    def exchange_token(self, code, state: str = None):
        print(code, state)
        self.server().shutdown()
        self.server.shutdown()

    def request_authorize(self):
        res = requests.get(YUQUE_OAUTH_AUTHORIZE_URL,
                           params={'client_id': 'TSJjgMa1QIj5acgAHcvF', 'scope': 'doc,repo,group:read',
                                   'redirect_uri': 'http://localhost:8080/a', 'state': '123', 'response_type': 'code'})

        print(res.text)
        pass


if __name__ == '__main__':
    SimpleYuQueOAuth.run()
