import pandas as pd
import requests as r
from bs4 import BeautifulSoup

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    response = r.get(data['categories_container_url'].values[0])
    soup = BeautifulSoup(response.text, 'html.parser')
    
    matching_div = soup.find('div', class_=data['categories_container'].values[0])

    if matching_div is None:
        raise "div not found error"
    
    else:
        results = []

        links = matching_div.find_all('a', href=True)
        
        for link in links:
            if link['href'] != '#':
                link_info = {
                    'supermarket_id': data['id'].values[0],
                    'description': link.get_text(strip=True),
                    'url': link['href'], 
                }
        
                results.append(link_info)
    
    return pd.DataFrame(results)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
