from typing import List, Dict

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs) -> List[List[Dict]]:
    # take in dataframe of category_urls and create list[dict]
    users = []
    metadata = []

    for i in range(3):
        i += 1
        users.append(dict(id=i, name=f'user_{i}'))
        metadata.append(dict(block_uuid=f'for_user_{i}'))

    return [
        users,
        metadata,
    ]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
