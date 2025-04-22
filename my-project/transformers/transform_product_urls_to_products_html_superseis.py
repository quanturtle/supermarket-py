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
    response = requests.get(data['url']).text
    
    product_html = {
        'supermarket_id': data['supermarket_id'],
        'html': response,
        'url': data['url'],
        'created_at': datetime.now().isoformat()
    }

    data['product_html'] = product_html

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
