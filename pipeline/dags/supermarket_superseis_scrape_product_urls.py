'''
DAG: supermarket_superseis_scrape_product_urls
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
import broker
from constants import *
from datetime import datetime
from bs4 import BeautifulSoup
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
TRANSFORM_STREAM_NAME = 'superseis_transform_product_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_STRING_IN_URL = 'products'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
)
def supermarket_superseis_scrape_product_urls():
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
            raise AirflowNotFoundException('No product URLs HTML found for Superseis in `product_urls_html` table.')

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
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
        
            if batch is None:
                break

            for product_url_html in batch:
                soup = BeautifulSoup(product_url_html['html'], 'html.parser')

                links = soup.find_all('a', href=True)

                product_urls = []

                for link in links:
                    if (PRODUCT_STRING_IN_URL in link['href'].lower()) and (link.get_text(strip=True) != ''):
                        product_url = {
                            'supermarket_id': product_url_html['supermarket_id'],
                            'description': link.get_text(strip=True),
                            'url': link['href'],
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


supermarket_superseis_scrape_product_urls()