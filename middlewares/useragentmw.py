# coding: utf8
# pylint:disable=unused-argument

"""
UserAgent中间件
"""

import random

MOBILE_USER_AGENT_LIST = [
        'Mozilla/5.0 (Linux; U; Android 4.0.1; ja-jp; Galaxy Nexus Build/ITL41D) AppleWebKit/534.30(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.1; ja-jp; Galaxy Nexus Build/JRO03H) AppleWebKit/534.30(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Android; Linux armv7l; rv:9.0) Gecko/20111216 Firefox/9.0 Fennec/9.0'
]

USER_AGENT_LIST = [
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Sa'
    'fari/537.17',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;'
    ' .NET CLR 3.0.30729; Media Center PC 6.0)',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
    'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox'
    '/2.0.0.6 Navigator/9.0b3',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13",
]


class RandomUserAgentMiddleware(object):

    """
    UserAgent中间件
    """

    def __init__(self, user_agent_list):
        '''
        初始化
        '''
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        """
        类构造
        """
        user_agent_mw = cls(USER_AGENT_LIST)
        return user_agent_mw

    def _get_user_agent(self):
        """
        随机UserAgent
        """
        return random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        """
        process request, 添加随机USER_AGENT
        """
        request.headers.setdefault("User-Agent", self._get_user_agent())

class RandomMobilUserAgentMiddleware(object):
    '''
    手机版的USER_AGENT中间件
    '''
    def __init__(self, user_agent_list):
        '''
        初始化
        '''
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        """
        类构造
        """
        user_agent_mw = cls(MOBILE_USER_AGENT_LIST)
        return user_agent_mw

    def _get_user_agent(self):
        """
        随机UserAgent
        """
        return random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        """
        process request, 添加随机USER_AGENT
        """
        request.headers.setdefault("User-Agent", self._get_user_agent())

