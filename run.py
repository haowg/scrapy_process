#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint:disable=relative-import
'''
入口文件
'''

import re
import glob
from multiprocessing import Process
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from excel import Excel
from conf import SPIDER_DIC, CUR

EXCEL_MAGANGER = Excel()


def __get_default_setting():
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


def _get_spider_process():
    '''
    配置并返回爬虫进程
    '''
    settings = __get_default_setting()
    # pipelines
    dict_pipelines = {}
    settings.set("ITEM_PIPELINES", dict_pipelines)
    dict_pipelines['pipelines.JsonWriterPipeline'] = 200
    # middlewares
    download_middlewares_dict = {
        "middlewares.useragentmw.RandomUserAgentMiddleware": 100,
        "middlewares.cookiejarmw.CookieMW":120
    }
    settings.set("DOWNLOADER_MIDDLEWARES", download_middlewares_dict)
    process = CrawlerProcess(settings)
    return process


def runspider(*args):
    """多进程"""
    proc = Process(target=__crawl, args=args)
    proc.start()
    proc.join()

def __crawl(spider, url, book_name):
    '''
    执行爬虫
    '''
    # 加载rule
    spider_process = _get_spider_process()
    spider_process.crawl(spider, url, book_name)
    spider_process.start()


def main():
    ''' 解析参数并运行相应的模式 '''
    runspider(
        SPIDER_DIC['qq'],
        'www.qq.com?book_id=123242',
        'asdfa'
    )


if __name__ == "__main__":
    '''
    main
    '''
    #urls = get_book_urls()
    #for url in urls:
    #    print url, urls.get(url)
    main()
