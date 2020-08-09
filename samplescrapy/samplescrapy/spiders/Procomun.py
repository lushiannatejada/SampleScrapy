# -*- coding: utf-8 -*-
import scrapy
from samplescrapy.product2 import ItemCompleted
from pymongo import MongoClient
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Identity, MapCompose
from w3lib.html import remove_tags
from scrapy.shell import inspect_response


class ProComun(scrapy.Spider):
    name = 'ProComun'
    start_urls = ['https://www.oercommons.org/browse?batch_size=20&sort_by=title&view_mode=summary&f.language=en']

    def parse(self, response):
        for commons in response.xpath('//li[@class="search-result ode-result clearfix"]'):
            loader = ItemLoader(item=ItemCompleted(), selector=commons)
            loader.add_xpath('link', './/h2[@class="title"]/a/@href')
            item = loader.load_item()
            www = 'http://procomun.educalab.es/'
            url = item['link'][0]
            return scrapy.Request(www + url, callback=self.parse_mongo, meta={'item': item})
        #cambiar paginacion
        next_page = response.xpath('//li[@class="pager-next"]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)


    def parse_mongo(self, response):
        inspect_response(response, self)
        for commons in response.xpath('//article[@class="clearfix center"]'):
            item = response.meta['item']
            itemnew = ItemLoader(item, selector=commons)
#            url = response.url
#            print('****************************')
#            print(url)
            itemnew.add_xpath('title', './/div[@class="detail-title"]/h1/text()')
            itemnew.add_xpath('overview', './/div[@class="detail-ode-description"]/p/text()')
            itemnew.add_xpath('subject', './/div[@class="detail-ode-knowledge-area clearfix"]/a/text()')
            itemnew.add_xpath('material_type', './/div[@class="detail-ode-resource-type clearfix"]/a/text()')
            itemnew.add_xpath('author', './/div[@class="detail-ode-authors"]/div/span/a/text()')
#            print("****************************")
            yield itemnew.load_item()