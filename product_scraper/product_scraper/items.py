# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductScraperItem(scrapy.Item):
    supermarket = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    current_price = scrapy.Field()