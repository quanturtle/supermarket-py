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
        response = r.get(row['categories_container_url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'soup: {soup}')
        
        class_list = row['categories_container'].split()
        print(f'class_list: {class_list}')
        
        matching_divs = []
        
        for tag in soup.find_all('div'):
            if tag.has_attr('class'):
                if all(cls in tag.get('class') for cls in class_list):
                    matching_divs.append(tag)
        
        print(f'matching_divs: {matching_divs}' )
        
        if len(matching_divs) != 1:
            continue
            # raise ValueError(f"Expected exactly one div with class {' '.join(class_list)}, but found {len(matching_divs)}")
        
        else:
            matching_div = matching_divs[0]
            links = matching_div.find_all('a', href=True)
            
            for link in links:
                if link['href'] != '#':
                    link_info = {
                        'supermarket_id': row['id'],
                        'description': link.get_text(strip=True),
                        'url': link['href'], 
                    }
            
                    all_links.append(link_info)
    
    return pd.DataFrame(all_links)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
