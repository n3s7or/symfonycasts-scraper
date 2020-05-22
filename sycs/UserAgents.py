import random
from enum import Enum


class UA(Enum):
    MOZILLA = 0
    CHROME = 1
    SAFARI = 2


USER_AGENTS = {
    UA.MOZILLA: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    UA.CHROME: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 '
               'Safari/537.36',
    UA.SAFARI: 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
               'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 '
}


def get_random_user_agent():
    return random.choice(list(USER_AGENTS.values()))


def get_user_agent(ua):
    return USER_AGENTS.get(ua)
