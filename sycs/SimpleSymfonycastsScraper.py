import requests
from bs4 import BeautifulSoup
import os
import logging
from .UserAgents import UserAgent


class SimpleSymfonycastScraper:

    def __init__(self, course, start=None, end=-1, debug=True):
        self.__session = None
        self.__token = None

        logging.basicConfig(
            format='%(asctime)s %(message)s',
            filename='scraper.log',
            level=logging.DEBUG if debug else logging.INFO
        )

        try:
            self.__user_email = os.environ['SCS_USER']
            self.__user_passw = os.environ['SCS_PASS']
        except KeyError:
            raise Exception('Username or password not provided as environment variables (SCS_USER and SCS_PASS).')

        self.__rango = {
            'start': start is not None if start else 1,
            'end': end
        }
        self.__curse = '/screencast/' + course

        # Constants
        self.__BASE_URL = 'https://symfonycasts.com'
        self.__LOGIN_URL = '/login'
        self.__LOGIN_CHECK = '/login_check'
        self.__DOWNLOAD_SUFFIX = '/download/video'

    def get_direct_links(self):
        with requests.Session() as self.__session:
            self.__token = self.__get_token(self.__get_page_dom(self.__BASE_URL + self.__LOGIN_URL))
            self.__authenticate()

            dynamic_suffix_links = self.__get_links(self.__get_page_dom(self.__BASE_URL + self.__curse))
            dynamic_download_links = list(self.__gen_dyn_down_link(dynamic_suffix_links))

            if self.__rango['end'] < 1:
                self.__rango['end'] = len(dynamic_download_links)

            for i in range(self.__rango['start'] - 1, self.__rango['end']):
                link = dynamic_download_links[i]
                res_head = self.__session.head(link)

                if res_head.status_code == requests.codes.forbidden:
                    raise Exception("You don't have privileges (%s)" % res_head.url)

                logging.debug('Headers from HEAD dynamic links')
                res_head = self.__session.head(res_head.headers['location'])
                logging.debug(res_head.headers)

                yield res_head.headers['location']

    def __gen_dyn_down_link(self, dsl):
        """Yields download dynamic links to chapter's video.

        Parameters
        ----------
        dsl : Generator
            Download suffixes
        """
        for i in dsl:
            yield self.__BASE_URL + i + self.__DOWNLOAD_SUFFIX

    def __get_links(self, html):
        chapter_list = html.find('ul', class_='chapter-list')
        chapter_list_item = chapter_list.find_all('li')
        for item in chapter_list_item:
            if item.a['class'][0] != 'js-no-follow-link':
                yield item.a['href']

    def __authenticate(self):
        data = {
            '_csrf_token': self.__token,
            '_email': self.__user_email,
            '_password': self.__user_passw,
            '_submit': '',
            '_target_pat': self.__BASE_URL
        }

        r = self.__session.post(self.__BASE_URL + self.__LOGIN_CHECK, data=data)

        if r.url == self.__BASE_URL + self.__LOGIN_URL:
            raise Exception('Invalid username or pass.')

    def __get_token(self, html):
        logging.debug(html)
        login_sub_btn = html.find(class_='login-submit-btn')
        return login_sub_btn.input['value']

    def __get_page_dom(self, url):
        headers = {
            'user-agent': UserAgent.MOZILLA.name
        }
        r = self.__session.get(url=url, headers=headers)
        return BeautifulSoup(r.text, 'html.parser')
