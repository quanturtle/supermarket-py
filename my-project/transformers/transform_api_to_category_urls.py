import pandas as pd
import requests as r
from bs4 import BeautifulSoup

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    all_links = []
    
    for idx, row in data.iterrows():
        response = r.get(row['api_url']).json()
            
        for record in response:
            link_info = {
                'supermarket_id': row['id'],
                'description': record['description'],
                'url': record['url'], 
            }
    
            all_links.append(link_info)
    
    return pd.DataFrame(all_links)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
