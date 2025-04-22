import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    category_urls_container_url = data['category_urls_container_url'].values[0]
    response = requests.get(category_urls_container_url).text
    
    return {
        'supermarket_id': 1,
        'html': response,
        'url': category_urls_container_url,
        'created_at': datetime.now().isoformat()
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
