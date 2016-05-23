#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint:disable=relative-import
'''
入口文件
'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


def get_default_setting():
    '''
    spider's defautl Settings
    '''
    settings = Settings()
    # crawl settings
    settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", 28)
    settings.set("CONCURRENT_REQUESTS_PER_IP", 23)
    retry_http_codes = (500, 502, 503, 504, 400, 408, 403, 404)
    settings.set("RETRY_HTTP_CODES", retry_http_codes)
    settings.set("RETRY_TIMES", 10)
    settings.set("COOKIES_ENABLED", True)
    settings.set("DOWNLOAD_DELAY", 0.3)
    settings.set("DOWNLOAD_TIMEOUT", 8)
    return settings


def get_spider_process(settings):
    '''
    返回爬虫进程
    '''
    return CrawlerProcess(settings)


def crawl(spider_process, spider, *args, **kargs):
    '''
    执行爬虫
    '''
    # 加载rule
    spider_process.crawl(spider, *args, **kargs)
    spider_process.start()
