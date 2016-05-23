# coding: utf-8
"""conf"""

import sqlite3

# from spiders import qq, chuangshi, dushu, hongxiu, qidian
from spiders import (QqSpider, ChuangshiSpider, DushuSpider, HuanxiaSpider,
                     QidianSpider, XxsySpider, YunchengSpider, YunqiSpider)

__CX = sqlite3.connect("spider.db")
CUR = __CX.cursor()
SPIDER_DIC = {
    "book.qq": QqSpider,
    "chuangshi.qq": ChuangshiSpider,
    "dushu.qq": DushuSpider,
    "novel.hongxiu": "",
    "www.qidian": QidianSpider,
    "www.xxsy": XxsySpider,
    "www.yuncheng": YunchengSpider,
}
