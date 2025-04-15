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
    print(f'SOUP: {soup}')

    product_container_tag = 'div'
    product_container_class = 'row ma-1'
    product_details = soup.find(product_container_tag, class_=product_container_class)
    # print(f'PRODUCT DETAILS: {product_details}')
    
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

    product_name_tag = 'span'
    product_name_class = 'link'

    product_sku_tag = 'div'
    product_sku_class = 'v-card__subtitle mt-0 pa-0 text-center text-sm-left'

    product_price_tag = 'p'
    product_price_class = 'priceArticle mb-0'

    try:
        product_description = (
            product_details
            .find(product_name_tag, class_=product_name_class)
            .text.strip()
            .upper()
        )
    except:
        product_description = None

    try:
        sku_text = product_details.find(product_sku_tag, class_=product_sku_class).text.strip()
        product_sku = ''.join(filter(str.isdigit, sku_text))
    except:
        product_sku = None

    try:
        price_text = product_details.find(product_price_tag, class_=product_price_class).text.strip()
        product_price = int(''.join(filter(str.isdigit, price_text)))
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