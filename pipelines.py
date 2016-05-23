# -*- coding: utf-8 -*-
# pylint:disable=unused-argument
'''
pipelines 处理获取的item
'''
import json
import codecs

import pymongo
from scrapy.exceptions import DropItem


class JsonWriterPipeline(object):
    '''
    存储到json文件
    '''
    def __init__(self):
        '''
        初始化方法，打开文件
        '''
        self.file = codecs.open('items.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        '''
        关闭json文件
        '''
        self.file.close()

    def process_item(self, item, spider):
        '''
        写入到json文件
        '''
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item



class MongoPipeline(object):
    '''
    利用mongodb中的数据过滤item，并将通过的数据存储到mongodb中
    '''
    def __init__(self, mongo_uri, mongo_db):
        '''
        init, 保存mongodb的配置
        '''
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        '''
        类方法，初始化pipeline
        '''
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', '192.168.6.183:27017'),
            mongo_db=crawler.settings.get('MONGODB_NAME', 'zy_crawler_test')
        )

    def close_spider(self, spider):
        '''
        关闭mongodb
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
        处理item
        '''
        if item is None:
            raise DropItem("item is None")
        self.db['result_online_%s'%item['site']].insert(dict(item))
        return item

