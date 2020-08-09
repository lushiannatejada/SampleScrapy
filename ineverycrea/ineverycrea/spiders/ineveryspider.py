# -*- coding: utf-8 -*-
import scrapy
from ineverycrea.items import ItemInevery
from pymongo import MongoClient
from scrapy.loader import ItemLoader

class CommonstestSpider(scrapy.Spider):
    name = 'ineverycrea'

#    allowed_domains = ['oercommons.org']
    start_urls = ['https://ineverycrea.net/comunidad/ineverycrea/recursos?pagina=1']

    def parse(self, response):
        for commons in response.xpath('//article[@class="resource"]'):
            item = ItemLoader(item=ItemInevery(), selector=commons)
            links = response.xpath('.//h3[@class="titular"]/a/@href').extract()
            for url in links:
                yield scrapy.Request(url, callback=self.parse_mongo, meta={'item': item})

        next_page = response.xpath('//a[@class="indiceNavegacion filtro  siguiente"]/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_mongo(self, response):
        for commons in response.xpath('//div[@class="container"]'):
            item = response.meta['item']
            itemnew = ItemLoader(item, selector=commons)
            itemnew.add_value('link', response.url)
            itemnew.add_xpath('title', './/h1[@class="titulo"]/text()')
            itemnew.add_xpath('overview', './/div[@class="contenido"]/p/text()')
            itemnew.add_xpath('subject', './/div[@class="contenidos cateti etiquetas"]//span/text()')
            itemnew.add_xpath('author', './/div[@class="contenidos cateti"]//a[@property="dc:creator"]/text()')
            print("****************************")
            yield itemnew.load_item()
