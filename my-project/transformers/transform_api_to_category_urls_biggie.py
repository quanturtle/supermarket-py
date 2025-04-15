import pandas as pd
import requests
from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    category_urls_container_url = data['api_url'].values[0]
    response = requests.get(category_urls_container_url)
    
    categories = response.json()['items']
    results = []

    limit = 50
    offset = 0
    for category in categories:
        slug = category['slug'].strip()
        category_url = f'https://api.app.biggie.com.py/api/articles?take={limit}&skip={offset}&classificationName={slug}'

        link_info = {
            'supermarket_id': data['id'].values[0],
            'description': category['name'].strip(),
            'url': category_url,
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
