'''
# supermarket_superseis_scrape_products_html
PRODUCT_URLS --> PRODUCTS_HTML
'''
import time
import broker
import requests
from constants import *
from datetime import datetime
from requests.exceptions import RequestException
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'products_html_stream'
TRANSFORM_STREAM_NAME = 'superseis_transform_products_html_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_products_html'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

DELAY_SECONDS = 0.5


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
    doc_md=__doc__
)
def supermarket_superseis_scrape_products_html():
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
    def extract_product_urls():
        try:
            hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

            sql = f'''
                SELECT supermarket_id, url
                FROM product_urls
                WHERE supermarket_id = {SUPERMARKET_ID}
                ORDER BY created_at;
            '''

            results = hook.get_records(sql)

            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()

            product_urls = []
            
            for row in results:
                product_urls.append({
                    'supermarket_id': row[0],
                    'url': row[1]
                })

            my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *product_urls)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [EXTRACT]')
            print(e)

        return


    @task()
    def transform_product_urls_to_products_html():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        try:
            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
            
                if batch is None:
                    break

                for product_url in batch:
                    try:
                        time.sleep(DELAY_SECONDS)
                        response = requests.get(product_url['url'], timeout=30)
                        html_content = response.text
                        
                    # except Exception as e:
                    #     print(e)
                    #     continue
                    
                    # except Exception as e:
                    #     print(e)
                    #     continue
                    
                    except Exception as e:
                        print(e)
                        continue
                    
                    product_html = {
                        'supermarket_id': product_url['supermarket_id'],
                        'html': html_content,
                        'url': product_url['url'],
                        'created_at': datetime.now().isoformat()
                    }

                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url['entry_id']])
                    my_broker.write(OUTPUT_STREAM_NAME, product_html)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)
        
        return


    setup = setup_transform_stream()
    extract = extract_product_urls()
    transform = transform_product_urls_to_products_html()

    setup >> extract >> transform


supermarket_superseis_scrape_products_html()