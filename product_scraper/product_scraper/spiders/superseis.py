import scrapy
import requests
from .supermarket import Supermarket
from bs4 import BeautifulSoup
import re

class SuperseisSpider(scrapy.Spider):
    name = "superseis"
    allowed_domains = ["www.superseis.com.py"]
    start_urls = []

    def start_requests(self):
        url = f'http://localhost:8000/api/link/?supermarket={Supermarket.SUPERSEIS}'
        resp = requests.get(url)
        resp_json = resp.json()

        for elem in resp_json:
            yield scrapy.Request(url=elem['url'], callback=self.parse_category)
    

    def parse_category(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        product_links = soup.find_all('a', class_= re.compile(r"^product-title-link"))     

        for link in product_links:
            if link.get('href') is not None:
                yield scrapy.Request(url=link.get('href'), callback=self.parse_product)


    def parse_product(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        supermarket = Supermarket.SUPERSEIS
        url = response.url
        sku = soup.find('div', class_=re.compile(r"^sku"))
        name = soup.find('h1', class_=re.compile(r"^productname"))
        price = soup.find('span', class_=re.compile(r"^productPrice"))

        sku = re.sub('[^0-9]+', '', re.sub('[^A-Za-z0-9]+', ' ', sku.text).strip())
        name = re.sub('[^A-Za-z0-9]+', ' ', name.text).strip()
        price = re.sub('[^0-9]+', '', re.sub('[^A-Za-z0-9]+', ' ', price.text).strip())

        product_data = {
            'supermarket': supermarket,
            'url': url,
            'sku': sku, 
            'name': name, 
            'current_price': price
        }

        resp = requests.post('http://localhost:8000/api/product/', data=product_data)        

        yield {
            'supermarket': supermarket,
            'url': url,
            'sku': sku, 
            'name': name, 
            'current_price': price,
            'resp': resp.status_code,
        }