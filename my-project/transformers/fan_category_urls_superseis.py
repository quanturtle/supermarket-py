import pandas as pd


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    data.drop_duplicates(subset='url', keep='first', inplace=True)

    category_urls = []
    metadata = []

    for idx, row in data.iterrows():
        category_urls.append({
            'id': idx,
            'url': row['url'],
            'supermarket_id': row['supermarket_id']
        })
        
        metadata.append({
            'block_uuid': f'visiting_{row["url"]}'
        })

    return [
        category_urls,
        metadata
    ]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
