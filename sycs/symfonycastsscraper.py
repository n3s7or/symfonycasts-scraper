import requests
from bs4 import BeautifulSoup
import os
from .sycsexceptions import *
from .requestshelper import RequestsHelper, Methods
from urllib.parse import urlparse

# Constants
BASE_URL = 'https://symfonycasts.com'
LOGIN_URL = '/login'
LOGIN_CHECK = '/login_check'
DOWNLOAD_SUFFIX = '/download/video'


class SimpleSymfonycastScraper:

    def __init__(self, course, start=None, end=None):

        self.request = RequestsHelper()

        self.range = {
            'start': start if start is not None else 1,
            'end': end if end is not None else -1
        }
        self.course = '/screencast/' + course

    def get_direct_links(self):
        r = self.request.call(url=BASE_URL + self.course, method=Methods.GET)
        if r.status_code == requests.codes.not_found:
            raise CourseNotFoundException

        dynamic_suffix_links = self.get_links(self.get_dom(r.text))
        dynamic_download_links = list(self.__gen_dyn_down_link(dynamic_suffix_links))

        num_videos = len(dynamic_download_links)
        if self.range['start'] > num_videos \
                or self.range['start'] < 1 \
                or (self.range['end'] != -1 and self.range['start'] > self.range['end']):
            raise WrongRangeException

        if self.range['end'] < 1 or self.range['end'] > num_videos:
            self.range['end'] = num_videos

        for i in range(self.range['start'] - 1, self.range['end']):
            link = dynamic_download_links[i]
            res_head = self.request.call(link, Methods.HEAD)

            if res_head.status_code == requests.codes.forbidden or urlparse(res_head.url).path == '/login':
                raise ForbiddenException

            yield res_head.url

    @staticmethod
    def __gen_dyn_down_link(dsl):
        """Yields download dynamic links to chapter's video."""
        for i in dsl:
            yield BASE_URL + i + DOWNLOAD_SUFFIX

    @staticmethod
    def get_links(html):
        chapter_list = html.find('ul', class_='chapter-list')
        chapter_list_item = chapter_list.find_all('li')
        for item in chapter_list_item:
            if item.a['class'][0] != 'js-no-follow-link':
                yield item.a['href']

    @staticmethod
    def get_token(html):
        login_sub_btn = html.find(class_='login-submit-btn')
        return login_sub_btn.input['value']

    @staticmethod
    def get_dom(text):
        return BeautifulSoup(text, 'html.parser')

    def authenticate(self):
        r = self.request.call(url=BASE_URL + LOGIN_URL, method=Methods.GET)
        token = self.get_token(self.get_dom(r.text))

        try:
            user_email = os.environ['SCS_USER']
            user_passw = os.environ['SCS_PASS']
        except KeyError:
            raise CredentialsException

        data = {
            '_csrf_token': token,
            '_email': user_email,
            '_password': user_passw,
            '_submit': '',
            '_target_pat': BASE_URL
        }

        url = BASE_URL + LOGIN_CHECK
        r = self.request.call(url=url, method=Methods.POST, data=data)
        if r.url == url:
            if r.status_code == requests.codes.too_many:
                raise TooManyException
            else:
                raise InvalidCredentialsException
