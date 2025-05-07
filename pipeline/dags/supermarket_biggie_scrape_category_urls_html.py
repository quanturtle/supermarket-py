'''
DAG: supermarket_biggie_scrape_category_urls_html
SUPERMARKETS --> CATEGORY_URLS_HTML
'''
import broker
import requests
from constants import *
from datetime import datetime
from requests.exceptions import Timeout, InvalidURL, HTTPError
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'category_urls_html_stream'
TRANSFORM_STREAM_NAME = 'biggie_transform_category_urls_html_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_category_urls_html'
SUPERMARKET_ID = SupermarketID.BIGGIE
SUPERMARKET_NAME = SupermarketName.BIGGIE
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def supermarket_biggie_scrape_category_urls_html():
    @task()
    def setup_transform_stream():
        try:
            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()
        
            my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)
        
        except:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [SETUP]')

        return
    
    @task()
    def extract_supermarkets():
        try:
            hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
            
            sql = f'''
                SELECT id, api_url
                FROM supermarkets
                WHERE name LIKE '{SUPERMARKET_NAME}'
                ORDER BY created_at;
            '''

            result = hook.get_first(sql)
            
            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()

            my_broker.write(TRANSFORM_STREAM_NAME, {
                'supermarket_id': result[0], 
                'url': result[1]
            })
        
        except:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [EXTRACT]')

        return


    @task()
    def transform_supermarkets_to_category_urls_html():
        try:
            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()        

            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)
            
                if batch is None:
                    break

                for supermarket in batch:
                    try:
                        resp = requests.get(supermarket['url'], timeout=30)
                    
                    except Timeout:
                        # error = 'request timed out'
                        continue

                    except InvalidURL:
                        # error = 'invalid url'
                        continue

                    except HTTPError:
                        # error = 'http error'
                        continue

                    category_urls_html = {
                        'supermarket_id': supermarket['supermarket_id'],
                        'html': resp.text,
                        'url': supermarket['url'],
                        'created_at': datetime.now().isoformat(),
                    }
                    
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[supermarket['entry_id']])
                    my_broker.write(OUTPUT_STREAM_NAME, category_urls_html)
        
        except:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
        
        return


    setup = setup_transform_stream()
    extract = extract_supermarkets()
    transform = transform_supermarkets_to_category_urls_html()

    setup >> extract >> transform


supermarket_biggie_scrape_category_urls_html()