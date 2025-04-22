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
    STREAM_NAME = 'category_urls_html_stream'
    
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    redis_conn.xadd(STREAM_NAME, {'data': json.dumps(data)})
    
    return {'status': 'completed'}