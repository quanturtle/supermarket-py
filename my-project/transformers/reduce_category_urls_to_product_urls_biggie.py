import time
import requests as r
from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque
from typing import Dict, List

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: Dict, *args, **kwargs) -> List[Dict]:
    visited_urls = set()
    queue = deque([data['url']])

    product_urls = []
    product_details = []

    offset = 0
    while queue:
        time.sleep(0.5)
        visiting_url = queue.popleft()
		
        response = r.get(visiting_url)
        visited_urls.add(visiting_url)

        try:
            product_list = response.json()['items']
        except:
            break
        
        if len(product_list) < 1:
            break
        
        else:
            for product in product_list:
                url_suffix = product['name'].replace('.', '') \
				                .replace(' ', '-') \
				                .replace('´', '').lower() + '-' + product['code']

                description = product['name'].strip()
                sku = product['code']
                price = product['price']
                url = f'https://biggie.com.py/item/{url_suffix}'
                created_at = datetime.now()

                product_url = {
                    'supermarket_id': data['supermarket_id'],
                    'description': description,
                    'url': url,
                    'created_at': created_at
                }
                
                product_detail = {
                    'supermarket_id': data['supermarket_id'],
                    'description': description,
                    'sku': sku,
                    'price': price,
                    'url': url,
                    'created_at': created_at
                }

                product_urls.append(product_url)
                product_details.append(product_detail)

            previous_offset_url = f'skip={offset}'
            offset += 50
            next_offset_url = f'skip={offset}'
            next_page = visiting_url.replace(previous_offset_url, next_offset_url)
            
            queue.append(next_page)

    data['product_urls'] = product_urls
    data['product_details'] = product_details

    return [data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
