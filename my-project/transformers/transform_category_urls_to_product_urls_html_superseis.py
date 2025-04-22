import time
from typing import Dict
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: Dict, *args, **kwargs):
    PAGINATION_STRING_IN_URL = 'pageindex'
    
    visited_urls = set()
    queue = deque([data['url']])

    product_urls_htmls = []

    while queue:
        time.sleep(0.5)
        visiting_url = queue.popleft()

        response = requests.get(visiting_url).text

        soup = BeautifulSoup(response, 'html.parser')
        
        links = soup.find_all('a', href=True)

        for link in links:
            if (PAGINATION_STRING_IN_URL in link['href'].lower()) and (link['href'] not in visited_urls):
                queue.append(link['href'])
                visited_urls.add(link['href'])

        product_urls_html = {
            'supermarket_id': data['supermarket_id'],
            'html': response,
            'url': visiting_url,
            'created_at': datetime.now().isoformat()
        }

        product_urls_htmls.append(product_urls_html)

    data['product_urls_htmls'] = product_urls_htmls

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
