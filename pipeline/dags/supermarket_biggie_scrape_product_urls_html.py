'''
# supermarket_biggie_scrape_product_urls_html_biggie
CATEGORY_URLS --> PRODUCT_URLS_HTML
'''
import time
import json
import broker
import requests
from constants import *
from datetime import datetime
from collections import deque
from requests.exceptions import Timeout, InvalidURL, HTTPError
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'product_urls_html_stream'
TRANSFORM_STREAM_NAME = 'biggie_transform_product_urls_html_stream'
ERROR_REQUEST_STREAM_NAME = 'error_request_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls_html_biggie'
SUPERMARKET_ID = SupermarketID.BIGGIE.value

BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000
DELAY_SECONDS = 0.5


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
    doc_md=__doc__
)
def supermarket_biggie_scrape_product_urls_html():
    @task()
    def setup_transform_stream():
        try:
            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()
            
            my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [SETUP]')
            print(e)
            
        return
    
    
    @task()
    def extract_category_urls():
        try:
            hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

            sql = f'''
                SELECT supermarket_id, url
                FROM category_urls
                WHERE supermarket_id = {SUPERMARKET_ID}
                ORDER BY created_at;
            '''

            results = hook.get_records(sql)

            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()

            category_urls = []
            
            for row in results:
                category_urls.append({
                    'supermarket_id': row[0],
                    'url': row[1]
                })
            
            my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *category_urls)

        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [EXTRACT]')
            print(e)

        return


    @task()
    def transform_category_urls_to_product_urls_html():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        try:
            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        

                if batch is None:
                    break
            
                for category_url in batch:
                    queue = deque([category_url['url']])
                    OFFSET = 0
                
                    while queue:
                        visiting_url = queue.popleft()
                        
                        try:
                            time.sleep(DELAY_SECONDS)
                            response = requests.get(visiting_url, timeout=30)
                            api_response = response.json()['items']
                        
                        except Timeout as to:
                            print(to)
                            my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': visiting_url, 'exception': 'request timed out', 'detail': to})
                            continue

                        except InvalidURL as iu:
                            print(iu)
                            my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': visiting_url, 'exception': 'invalid url', 'detail': iu})
                            continue

                        except HTTPError as ht:
                            print(ht)
                            my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': visiting_url, 'exception': 'http error', 'detail': ht})
                            continue

                        except Exception as e:
                            print(e)
                            my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': visiting_url, 'exception': 'uncaught exception', 'detail': e})
                            continue

                        if len(api_response) < 1:
                            break

                        product_url_html = {
                            'supermarket_id': category_url['supermarket_id'],
                            'html': json.dumps(api_response),
                            'url': visiting_url,
                            'created_at': datetime.now().isoformat()
                        }

                        my_broker.write(OUTPUT_STREAM_NAME, product_url_html)

                        previous_offset = f'skip={OFFSET}'
                        OFFSET += 50
                        next_offset = f'skip={OFFSET}'
                        next_page = visiting_url.replace(previous_offset, next_offset)

                        queue.append(next_page)

                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[category_url['entry_id']])

        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)
        
        return
    

    setup = setup_transform_stream()
    extract = extract_category_urls()
    transform = transform_category_urls_to_product_urls_html()

    setup >> extract >> transform


supermarket_biggie_scrape_product_urls_html()