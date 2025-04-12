import re
import requests as r
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: Dict, *args, **kwargs) -> List[Dict]:		
    response = r.get(data['url'])

    soup = BeautifulSoup(response.text, 'html.parser')

    # product
    product_description = soup.select_one('h1.productname[itemprop="name"]').text.strip().upper()
    
    product_sku = soup.select_one('div.sku[itemprop="sku"]').text.strip()
    product_sku = ''.join(filter(str.isdigit, product_sku))
    
    product_price_span = soup.select_one('span.productPrice').text.strip()
    product_price = int(''.join(filter(str.isdigit, product_price_span)))
    
    product_info = {
        'supermarket_id': data['supermarket_id'],
        'description': product_description,
        'sku': product_sku,
        'price': product_price,
        'created_at': datetime.now()
    }
    
    data['product_info'] = product_info
    
    return [data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
