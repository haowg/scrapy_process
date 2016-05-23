#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint:disable=relative-import
'''
入口文件
'''
import sys

from multiprocessing import Process

from conf import SPIDER_DIC
from spider_process import get_default_setting, get_spider_process, crawl


def spider_settings(settings):
    dict_pipelines = {}
    settings.set("ITEM_PIPELINES", dict_pipelines)
    dict_pipelines['pipelines.JsonWriterPipeline'] = 200
    # middlewares
    download_middlewares_dict = {
        "middlewares.useragentmw.RandomUserAgentMiddleware": 100,
        "middlewares.cookiejarmw.CookieMW": 120
    }
    settings.set("DOWNLOADER_MIDDLEWARES", download_middlewares_dict)
    return settings


def runspider(*args):
    """多进程"""
    proc = Process(target=crawl, args=args)
    proc.start()
    proc.join()


def main():
    ''' 解析参数并运行相应的模式 '''

    settings = spider_settings(get_default_setting())
    runspider(
        get_spider_process(settings),
        SPIDER_DIC['qq'],
        'www.qq.com?book_id=123242',
        'asdfa'
    )


if __name__ == "__main__":
    '''
    main
    '''
    sys.exit(main())
