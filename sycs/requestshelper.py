from enum import Enum

import requests
from .useragents import get_random_user_agent


class Methods(Enum):
    GET = 'get'
    POST = 'post'
    HEAD = 'head'


class RequestsHelper(object):
    """Class to handle all http request routines."""

    def __init__(self, useragent=None):
        self.session = requests.Session()
        self.token = None
        self.headers = {
            'user-agent': useragent if useragent is not None else get_random_user_agent()
        }

    def call(self, url, method=Methods.GET, data=None):
        return self.session.request(method=method.name, url=url, headers=self.headers, data=data)
