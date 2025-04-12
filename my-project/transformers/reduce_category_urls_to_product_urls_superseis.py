import time
import requests as r
from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque
from typing import Dict, List

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: Dict, *args, **kwargs) -> List[Dict]:
    visited_urls = set()
    queue = deque([data['url']])

    results = []

    while queue:
        time.sleep(1)
        url = queue.popleft()
		
        response = r.get(url)
        visited_urls.add(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
	
        for link in links:
            if (link['href'] != '#') and ('products' in link['href']):
                link_info = {
                    'supermarket_id': data['supermarket_id'],
                    'description': link.get_text(strip=True),
                    'url': link['href'],
                    'created_at': datetime.now()
                }
				
                results.append(link_info)

            else:
                if ('pageindex' in link['href'].lower()) and (link['href'] not in visited_urls):
                    queue.append(link['href'])
                    visited_urls.add(link['href'])

    data['product_links'] = results
    
    return [data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
