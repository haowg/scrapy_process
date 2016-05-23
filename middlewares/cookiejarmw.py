# coding: utf-8
"""cookie 中间件"""

class CookieMW(object):
    """cookie middlewares"""
    def process_request(self, request, spider):
        """process request"""
        request.meta['cookiejar'] = 1
