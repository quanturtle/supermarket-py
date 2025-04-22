import os
import json
import redis

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    STREAM_NAME = os.getenv("STREAM_NAME", "products_stream")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    pipe = redis_conn.pipeline()

    product = {
        "supermarket_id": 1,
        "description": "Test Product XXX",
        "sku": "SKU_XXX",
        "price": 99.99,
        "url": f"http://example.com/product/XXXX"
    }

    pipe.xadd(STREAM_NAME, {'data': json.dumps(product)})

    pipe.execute()
    
    return {'hello': 'yes'}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'