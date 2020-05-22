import requests
from bs4 import BeautifulSoup
import os
import logging
from .UserAgents import get_random_user_agent
from .SYCSExceptions import CredentialsException, WrongRangeException, ForbiddenException


# Constants
BASE_URL = 'https://symfonycasts.com'
LOGIN_URL = '/login'
LOGIN_CHECK = '/login_check'
DOWNLOAD_SUFFIX = '/download/video'


class SimpleSymfonycastScraper:

    def __init__(self, course, start=None, end=None, debug=True):
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            filename='scraper.log',
            level=logging.DEBUG if debug else logging.INFO
        )

        try:
            self.__user_email = os.environ['SCS_USER']
            self.__user_passw = os.environ['SCS_PASS']
        except KeyError:
            raise CredentialsException

        self.__session = None
        self.__token = None
        self.__useragent = get_random_user_agent()

        self.__range = {
            'start': start if start is not None else 1,
            'end': end if end is not None else -1
        }
        self.__curse = '/screencast/' + course

    def get_direct_links(self):
        with requests.Session() as self.__session:
            self.__token = self.get_token(self.__get_page_dom(BASE_URL + LOGIN_URL))
            self.__authenticate()

            dynamic_suffix_links = self.get_links(self.__get_page_dom(BASE_URL + self.__curse))
            dynamic_download_links = list(self.__gen_dyn_down_link(dynamic_suffix_links))

            num_videos = len(dynamic_download_links)
            if self.__range['start'] > num_videos \
                    or self.__range['start'] < 1 \
                    or (self.__range['end'] != -1 and self.__range['start'] > self.__range['end']):
                raise WrongRangeException

            if self.__range['end'] < 1 or self.__range['end'] > num_videos:
                self.__range['end'] = num_videos

            for i in range(self.__range['start'] - 1, self.__range['end']):
                link = dynamic_download_links[i]
                res_head = self.__session.head(link)

                if res_head.status_code == requests.codes.forbidden:
                    raise ForbiddenException

                res_head = self.__session.head(res_head.headers['location'])
                logging.debug(res_head.headers)

                yield res_head.headers['location']

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
        logging.debug(html)
        login_sub_btn = html.find(class_='login-submit-btn')
        return login_sub_btn.input['value']

    def __authenticate(self):
        data = {
            '_csrf_token': self.__token,
            '_email': self.__user_email,
            '_password': self.__user_passw,
            '_submit': '',
            '_target_pat': BASE_URL
        }

        r = self.__session.post(BASE_URL + LOGIN_CHECK, data=data)

        if r.url == BASE_URL + LOGIN_URL:
            raise Exception('Invalid username or pass.')

    def __get_page_dom(self, url):
        headers = {
            'user-agent': self.__useragent
        }
        r = self.__session.get(url=url, headers=headers)
        return BeautifulSoup(r.text, 'html.parser')
