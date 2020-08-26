# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class DemoItem(scrapy.Item):
    title = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    link = Field()
    overview = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    subject = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    material_type = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    level = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())