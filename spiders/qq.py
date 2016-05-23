# -*- coding: utf-8 -*-
import re
import json
import requests

from lxml import etree

import scrapy
from content import BookContentItem, ContentSpider
from scrapy.http import FormRequest


class QqSpider(ContentSpider):
    """qq spider"""
    name = "qq"
    allowed_domains = ["book"]

    def __init__(self, book_url, book_name):
        """初始化"""
        super(QqSpider, self).__init__(book_url, book_name)

    def start_requests(self):
        """start"""
        cookie_json = json.loads(file('cookies/qq.cookie').read())
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=cookie_json)

    def get_chapter_urls(self, response):
        """获取图书章节链接"""
        bid = re.findall(r'bid="(\d+)"', response.body)[0]
        chapter_url = 'http://book.qq.com/intro/listcontent.html'
        page_index = 1
        while 1:
            post_data = {'bid': bid, 'pageIndex': page_index}
            resp = requests.post(chapter_url, data=post_data)
            data = json.loads(resp.content)
            if data.get('PageCount') < page_index:
                break
            for url in etree.HTML(data.get('ListHTMl')).xpath(r'//a/@href'):
                content_url = 'http://book.qq.com/read/{bid}/{cid}'.format(
                    bid=bid, cid=url.split('cid=')[-1])
                yield content_url
            page_index += 1

    def get_content(self, response):
        """返回内容"""
        item = BookContentItem()
        content_html = etree.HTML(json.loads(response.body).get('Content'))
        content = ''.join(content_html.xpath(
            '//div[@class="bookreadercontent"]//text()'))
        item['content'] = content
        item['title'] = content_html.xpath('//h1/text()')[0]
        item['url'] = response.url
        item['book_name'] = self.book_name
        return item

    def combin_request(self, url, response):
        body = '_token=%s&fontsize=14&lang=&w=830'% response.request.cookies[-2].get('value')
        return scrapy.Request('%s?%s' % (url, body),
                              method='get',
                              callback=self.get_content,
                              dont_filter=True,)
