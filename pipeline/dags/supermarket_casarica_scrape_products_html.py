'''
DAG: supermarket_casarica_scrape_products_html
PRODUCT_URLS --> PRODUCTS_HTML
'''
import broker
from datetime import datetime
import requests
from requests.exceptions import RequestException
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.postgres.hooks.postgres import PostgresHook
import time


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'products_html_stream'
TRANSFORM_STREAM_NAME = 'casarica_transform_products_html_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

SUPERMARKET_ID = 5
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000
DELAY_SECONDS = 0.5


@dag(
    default_args=DEFAULT_ARGS,
    tags=['casarica', 'etl'],
    catchup=False,
)
def supermarket_casarica_scrape_products_html():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return
    
    
    @task()
    def extract_product_urls():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = f'''
            SELECT supermarket_id, url
            FROM product_urls
            WHERE supermarket_id = {SUPERMARKET_ID}
            ORDER BY created_at;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No product URLs found for casarica in `product_urls` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        product_urls = []
        
        for row in results:
            product_urls.append({
                'supermarket_id': row[0],
                'url': row[1]
            })

        my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *product_urls)

        return


    @task()
    def transform_product_urls_to_products_html():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
        
            if batch is None:
                break

            for product_url in batch:
                try:
                    time.sleep(DELAY_SECONDS)
                    
                    response = requests.get(product_url['url'], timeout=30)
                    response.raise_for_status()
                    html_content = response.text
                    
                    product_html = {
                        'supermarket_id': product_url['supermarket_id'],
                        'html': html_content,
                        'url': product_url['url'],
                        'created_at': datetime.now().isoformat()
                    }
                    
                except RequestException as e:
                    print(f'Failed to fetch URL {product_url['url']}: {e}')
                    
                    return {'error': str(e)}

                my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url['entry_id']])
                my_broker.write(OUTPUT_STREAM_NAME, product_html)
        
        return


    setup = setup_transform_stream()
    extract = extract_product_urls()
    transform = transform_product_urls_to_products_html()

    setup >> extract >> transform


supermarket_casarica_scrape_products_html()