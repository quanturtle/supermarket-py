'''
DAG: supermarket_biggie_scrape_product_urls
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
import re
import unicodedata
from datetime import datetime
import json
import broker
from constants import *
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'product_urls_stream'
TRANSFORM_STREAM_NAME = 'biggie_transform_product_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls'
SUPERMARKET_ID = SupermarketID.BIGGIE
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def supermarket_biggie_scrape_product_urls():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return


    @task()
    def extract_product_urls_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = f'''
            SELECT supermarket_id, html, url
            FROM product_urls_html
            WHERE supermarket_id = {SUPERMARKET_ID}
            ORDER BY created_at;
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


    def create_url_suffix(name, code):
        name = str(name).replace('‘', "'").replace('´', '')
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
        name = re.sub(r'[./%]', '', name)
        slug = re.sub(r'\s+', '-', name).strip('-')

        return f"{slug}-{code}"


    @task()
    def transform_product_urls_html_to_product_urls():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
        
            if batch is None:
                break

            for product_url_html in batch:
                product_urls_html = json.loads(product_url_html['html'])

                product_urls = []

                for item in product_urls_html:
                    url_suffix = create_url_suffix(item['name'], item['code'])
                    
                    product_url = {
                        'supermarket_id': product_url_html['supermarket_id'],
                        'description': item['name'].strip().upper(),
                        'url': f'https://biggie.com.py/item/{url_suffix}'.strip(),
                        'created_at': datetime.now().isoformat()
                    }
                    print(product_url)

                    product_urls.append(product_url)

                my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url_html['entry_id']])
                my_broker.write_pipeline(OUTPUT_STREAM_NAME, *product_urls)

        return

    
    setup = setup_transform_stream()
    extract = extract_product_urls_html()
    transform = transform_product_urls_html_to_product_urls()

    setup >> extract >> transform


supermarket_biggie_scrape_product_urls()