import time
from typing import Dict
import requests
from datetime import datetime
from bs4 import BeautifulSoup


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: Dict, *args, **kwargs):
    PRODUCT_STRING_IN_URL = 'products'

    soup = BeautifulSoup(data['html'], 'html.parser')
    
    links = soup.find_all('a', href=True)

    product_urls = []
    
    for link in links:
        if (PRODUCT_STRING_IN_URL in link['href'].lower()) and (link.get_text(strip=True) != ''):
            product_url = {
                'supermarket_id': data['supermarket_id'],
                'description': link.get_text(strip=True),
                'url': link['href'],
                'created_at': datetime.now().isoformat()
            }

            product_urls.append(product_url)

    data['product_urls'] = product_urls

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
