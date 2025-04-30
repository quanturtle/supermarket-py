'''
DAG: scrape_category_urls_html_biggie
SUPERMARKETS --> CATEGORY_URLS_HTML
'''
from datetime import datetime
import requests
import broker
import json
from requests.exceptions import RequestException
from redis.exceptions import ResponseError
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'category_urls_html_stream'
TRANSFORM_STREAM_NAME = 'transform_category_urls_html_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def scrape_category_urls_html_biggie():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return
    
    @task()
    def extract_supermarkets():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = '''
            SELECT id, api_url
            FROM supermarkets
            WHERE name LIKE 'Biggie'
            LIMIT 1;
        '''

        result = hook.get_first(sql)

        if not result:
            raise AirflowNotFoundException('No Biggie row found in `supermarkets` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        my_broker.write(TRANSFORM_STREAM_NAME, {
            'supermarket_id': result[0], 
            'url': result[1]
        })

        return


    @task()
    def transform_supermarkets_to_category_urls_html():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=20, block_time_ms=5_000)
        
            if batch is None:
                break

            for supermarket in batch:
                url = supermarket.get('url')
                supermarket_id = supermarket.get('supermarket_id')

                if not url:
                    raise ValueError(
                        f'Missing "api_url" for supermarket ID {supermarket_id}'
                    )
            
                try:
                    resp = requests.get(url, timeout=30)
                    resp.raise_for_status()
                
                except RequestException as e:
                    print(f"Failed to fetch URL {url}: {e}")
                    raise
            
                category_urls_html = {
                    'supermarket_id': supermarket['supermarket_id'],
                    'html': resp.text,
                    'url': supermarket['url'],
                    'created_at': datetime.now().isoformat(),
                }
                
                my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[supermarket['entry_id']])
                my_broker.write(OUTPUT_STREAM_NAME, category_urls_html)

        return


    setup = setup_transform_stream()
    extract = extract_supermarkets()
    transform = transform_supermarkets_to_category_urls_html()

    setup >> extract >> transform


scrape_category_urls_html_biggie()


# import pandas as pd
# import requests
# from datetime import datetime

# if 'transformer' not in globals():
#     from mage_ai.data_preparation.decorators import transformer
# if 'test' not in globals():
#     from mage_ai.data_preparation.decorators import test


# @transformer
# def transform(data, *args, **kwargs):
#     category_urls_container_url = data['api_url'].values[0]
#     response = requests.get(category_urls_container_url)
    
#     categories = response.json()['items']
#     results = []

#     limit = 50
#     offset = 0
#     for category in categories:
#         slug = category['slug'].strip()
#         category_url = f'https://api.app.biggie.com.py/api/articles?take={limit}&skip={offset}&classificationName={slug}'

#         link_info = {
#             'supermarket_id': data['id'].values[0],
#             'description': category['name'].strip(),
#             'url': category_url,
#             'created_at': datetime.now()
#         }

#         results.append(link_info)
    
#     return pd.DataFrame(results)


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'