import os
import json
import redis
import pandas as pd


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data: pd.DataFrame, *args, **kwargs):
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    STREAM_NAME = 'category_urls_stream'
    
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    pipeline = redis_conn.pipeline()

    for idx, category_url in data.iterrows():
        pipeline.xadd(STREAM_NAME, {'data': json.dumps(category_url.to_dict())})

    pipeline.execute()
    
    return {'status': 'completed'}