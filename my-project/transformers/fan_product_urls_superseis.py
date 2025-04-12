import pandas as pd
from typing import List, Dict

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs) -> List[List[Dict]]:
    product_urls = []
    metadata = []

    for idx, row in data.iterrows():
        product_urls.append(dict(id=idx, url=row['url'], supermarket_id=row['supermarket_id']))
        metadata.append(dict(block_uuid=f'for_url_{idx}'))

    return [
        product_urls,
        metadata,
    ]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
