import scrapy
from scrapy.item import Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.spiders.crawl import identity
from w3lib.html import remove_tags


class ItemCompleted(scrapy.Item):
    title = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = Field()
    overview = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    subject = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    material_type = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    author = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    level = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())