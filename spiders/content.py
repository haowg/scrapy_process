# -*- coding: utf-8 -*-
import scrapy

class BookContentItem(scrapy.Item):
    """"""
    content = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    book_name = scrapy.Field()


class ContentSpider(scrapy.Spider):

    def __init__(self, book_url, book_name):
        """内容爬虫初始化"""
        if isinstance(book_url, basestring):
            self.start_urls = (book_url,)
        elif hasattr(book_url, '__iter__'):
            self.start_urls = book_url
        else:
            raise TypeError('start_urls type error')
        self.book_name = book_name
        super(ContentSpider, self).__init__()

    def parse(self, response):
        """parse"""
        chapter_response = self.get_chapter_resp(response)
        for url in self.get_chapter_urls(chapter_response):
            print url
            # todo 获取图书内容页面
            yield self.combin_request(url, response)

    def combin_request(self, url, response):
        """组合request"""
        return scrapy.Request(url,
                              callback=self.get_content,
                              dont_filter=True,
                              cookies=response.request.cookies
                              )

    def get_chapter_resp(self, response):
        """返回章节内容页面"""
        return response

    def get_chapter_urls(self, response):
        """返回章节url"""
        return response.xpath('//li//a/@href').extract()

    def get_content(self, response):
        """返回内容"""
        item = BookContentItem()
        item['content'] = response.xpath('//text()')
        item['book_name'] = self.book_name
        return item
