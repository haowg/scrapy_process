# coding: utf8
# pylint:disable=unused-argument,too-few-public-methods

"""
代理中间件
"""

from .proxymanager import ProxyManager


class ProxyMiddleware(object):

    """
    代理中间件
    """

    def __init__(self):
        self.proxy_manager = ProxyManager("/tmp/proxy_list.txt", 6)

    def process_request(self, request, spider):
        """process request
        """
        request.meta["proxy"] = self.proxy_manager.get_proxy()

class ProxyMiddleware_new(object):

    """
    代理中间件
    """

    def __init__(self):
        self.proxy = 'http://192.168.6.160:3128'

    def process_request(self, request, spider):
        """process request
        """
        request.meta["proxy"] = self.proxy

