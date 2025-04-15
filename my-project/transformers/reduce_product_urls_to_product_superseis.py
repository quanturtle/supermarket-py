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
    
    product_container_tag = 'div'
    product_container_class = 'product-details-info'
    product_details = soup.find(product_container_tag, class_=product_container_class)
    
    if not product_details:
        data['product_info'] = {
            'supermarket_id': data['supermarket_id'],
            'description': '',
            'sku': '',
            'price': '',
            'url': data['url'],
            'created_at': datetime.now()
        }

        return [data]

    product_name_tag = 'h1'
    product_name_class = 'productname'
    product_name_attrs = {'itemprop': 'name'}
    
    product_sku_tag = 'div'
    product_sku_class = 'sku'
    product_sku_attrs = {'itemprop': 'sku'}

    product_price_tag = ['div', 'span']
    product_price_class = ['price', 'productPrice']
    product_price_attrs = [{'itemprop': 'price'}, '']

    try:        
        product_description = product_details.find(product_name_tag, class_=product_name_class, attrs=product_name_attrs).text.strip().upper()
    except:
        product_description = None

    try:
        product_sku = product_details.find(product_sku_tag, class_=product_sku_class, attrs=product_sku_attrs).text.strip()
        product_sku = ''.join(filter(str.isdigit, product_sku))
    except:
        product_sku = None

    try:
        product_price_span = product_details.find(product_price_tag[0], class_=product_price_class[0], attrs=product_price_attrs[0]) \
                                .find(product_price_tag[1], class_=product_price_class[1]).text.strip()
        product_price = int(''.join(filter(str.isdigit, product_price_span)))
    except:
        product_price = None
    
    product_info = {
        'supermarket_id': data['supermarket_id'],
        'description': product_description,
        'sku': product_sku,
        'price': product_price,
        'url': data['url'],
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
