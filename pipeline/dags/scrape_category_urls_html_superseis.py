'''
DAG: scrape_category_urls_html_superseis
SUPERMARKETS --> CATEGORY_URLS_HTML
'''
from datetime import datetime
import requests
import broker
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
    tags=['superseis', 'etl'],
    catchup=False,
)
def scrape_category_urls_html_superseis():
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
            SELECT id, category_urls_container_url
            FROM supermarkets
            WHERE name LIKE 'Superseis'
            LIMIT 1;
        '''

        result = hook.get_first(sql)

        if not result:
            raise AirflowNotFoundException('No Superseis row found in `supermarkets` table.')

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
                        f'Missing "category_urls_container_url" for supermarket ID {supermarket_id}'
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


scrape_category_urls_html_superseis()