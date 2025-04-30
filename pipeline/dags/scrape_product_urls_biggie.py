'''
DAG: scrape_product_urls_biggie
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
from datetime import datetime
import json
import broker
from requests.exceptions import RequestException
from redis import RedisError
from redis.exceptions import ResponseError
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from bs4 import BeautifulSoup


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'product_urls_stream'
TRANSFORM_STREAM_NAME = 'transform_product_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def scrape_product_urls_biggie():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return


    @task()
    def extract_product_urls_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = '''
            SELECT supermarket_id, html, url
            FROM product_urls_html
            WHERE supermarket_id = 3
            LIMIT 1;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No product URLs HTML found for biggie in `product_urls_html` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        product_urls_html = []
        
        for row in results:
            product_urls_html.append({
                'supermarket_id': row[0],
                'html': row[1],
                'url': row[2],
            })

        my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *product_urls_html)

        return


    @task()
    def transform_product_urls_html_to_product_urls():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=20, block_time_ms=5_000)        
        
            if batch is None:
                break

            for product_url_html in batch:
                product_urls_html = json.loads(product_url_html['html'])

                product_urls = []

                for item in product_urls_html:
                    url_suffix = item['name'].replace('.', '') \
				                .replace(' ', '-') \
				                .replace('´', '').lower() + '-' + item['code']
                    
                    product_url = {
                        'supermarket_id': product_url_html['supermarket_id'],
                        'description': item['name'].strip().upper(),
                        'url': f'https://biggie.com.py/item/{url_suffix}',
                        'created_at': datetime.now().isoformat()
                    }

                    product_urls.append(product_url)

            my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url_html['entry_id']])
            my_broker.write_pipeline(OUTPUT_STREAM_NAME, *product_urls)

        return

    
    setup = setup_transform_stream()
    extract = extract_product_urls_html()
    transform = transform_product_urls_html_to_product_urls()

    setup >> extract >> transform


scrape_product_urls_biggie()