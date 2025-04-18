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
    response = requests.get(category_urls_container_url)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    
    results = []
    
    category_string_in_url = 'category'
    for link in links:
        if link['href'] != '#' and category_string_in_url in link['href']:
            link_info = {
                'supermarket_id': data['id'].values[0],
                'description': link.get_text(strip=True),
                'url': link['href'],
                'created_at': datetime.now()
            }
    
            results.append(link_info)
    
    return pd.DataFrame(results)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
