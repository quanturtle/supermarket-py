import os
import pandas as pd
import redis


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    data.drop_duplicates(subset='url', keep='first', inplace=True)

    product_urls_html = []
    metadata = []

    for idx, row in data.iterrows():
        product_urls_html.append({
            'id': idx,
            'html': row['html'],
            'url': row['url'],
            'supermarket_id': row['supermarket_id']
        })
        
        metadata.append({
            'block_uuid': f'visiting_{idx}'
        })

    return [
        product_urls_html,
        metadata
    ]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
