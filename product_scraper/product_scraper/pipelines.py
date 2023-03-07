# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests

class ProductScraperPipeline:
    def __init__(self):
        self.session = requests.Session()

    def process_item(self, item, spider):
        resp = self.session.post('http://localhost:8000/api/product/', data=item)        

        return item
