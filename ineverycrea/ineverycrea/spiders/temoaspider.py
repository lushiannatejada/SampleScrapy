# -*- coding: utf-8 -*-
import scrapy
from ineverycrea.product import TextItem
from scrapy.loader import ItemLoader

class TemoaSpider(scrapy.Spider):
    name = 'temoaself'

#    allowed_domains = ['temoa.tec.mx']
    start_urls = ['http://temoa.tec.mx/search/apachesolr_search/?filters=tid%3A30724%20tid%3A11']
    def parse(self, response):
        for temoa in response.xpath('//div[@class="search-snippet"]'):
            l = ItemLoader(item=TextItem(), selector=temoa)
            l.add_xpath('link', './/div[@class="node clear-block node-type-link"]/h1/a/@href')
            item = l.load_item()
            www = 'http://temoa.tec.mx'
            url = item['link'][0]
#            print(url)
            yield scrapy.Request(www + url, callback=self.parse_mongo, meta={'item': item})

        next_page = response.xpath('//li[@class="pager-next"]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_mongo(self, response):
        for commons in response.xpath('//div[@id="main"]'):
            item = response.meta['item']
            new = ItemLoader(item, selector=commons)
            new.add_xpath('title', './/h1[@class="title"]/text()')
            new.add_xpath('overview', './/div[@class="body expandable-long"]/text()')
            new.add_xpath('subject', './/div[@class="field field-type-content-taxonomy field-field-29-0"]'
                                     '//div[@class="field-item  odd"]/a/text()')
            new.add_xpath('material_type', './/div[@class="field field-type-content-taxonomy field-field-410"]'
                                           '//div[@class="field-item  odd"]/a/text()')
            new.add_xpath('author', './/span[@class="submitted"]/a/text()')
#            new.replace_value('link', response.url)
            print(response.url)
            yield new.load_item()

