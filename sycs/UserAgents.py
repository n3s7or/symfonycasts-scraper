from enum import Enum


class UserAgent(Enum):
    MOZILLA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
    CHROME = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 ' \
             'Safari/537.36'
    SAFARI = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, ' \
             'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 '
