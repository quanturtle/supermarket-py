import os
import json
import redis
from typing import Dict


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data: Dict, *args, **kwargs):
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    STREAM_NAME = 'product_urls_html_stream'
    
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    pipeline = redis_conn.pipeline()

    for product_urls_html in data['product_urls_htmls']:
        pipeline.xadd(STREAM_NAME, {'data': json.dumps(product_urls_html)})

    pipeline.execute()
    
    return