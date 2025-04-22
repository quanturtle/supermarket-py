from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    CATEGORY_STRING_IN_URL = 'category'
    RAW_HTML = data['html'].values[0]

    soup = BeautifulSoup(RAW_HTML, 'html.parser')
    links = soup.find_all('a', href=True)
    
    category_urls = []
    
    for link in links:
        if link['href'] != '#' and CATEGORY_STRING_IN_URL in link['href']:
            supermarket_id = data['supermarket_id'].values[0]
            description = link.get_text(strip=True)
            url = link['href']
            created_at = datetime.now().isoformat()
            
            category_url = {
                'supermarket_id': supermarket_id,
                'description': description,
                'url': url,
                'created_at': created_at
            }
    
            category_urls.append(category_url)
    
    return pd.DataFrame(category_urls)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
