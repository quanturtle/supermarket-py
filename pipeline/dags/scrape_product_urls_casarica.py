'''
DAG: scrape_product_urls_casarica
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
from datetime import datetime
import broker
from requests.exceptions import RequestException
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

PRODUCT_STRING_IN_URL = 'products'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['casarica', 'etl'],
    catchup=False,
)
def scrape_product_urls_casarica():
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
            WHERE supermarket_id = 5
            LIMIT 1;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No product URLs HTML found for casarica in `product_urls_html` table.')

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
                soup = BeautifulSoup(product_url_html['html'], 'html.parser')
                product_div = soup.find('div', class_='tab-content')
                
                links = product_div.find_all('a', href=True)

                product_urls = []

                for link in links:
                    if link['href'] not in ['javascript:void(0);', 'mi-lista']:
                        description = link.find('h2', class_='ecommercepro-loop-product__title')
                        product_url = {
                            'supermarket_id': product_url_html['supermarket_id'],
                            'description': description.get_text(strip=True) if description else '',
                            'url': f'https://www.casarica.com.py/{link['href']}',
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


scrape_product_urls_casarica()