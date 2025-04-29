'''
DAG: scrape_product_urls_html_superseis
CATEGORY_URLS --> PRODUCT_URLS_HTML
'''
import broker
from datetime import datetime
import requests
from requests.exceptions import RequestException
from redis import RedisError
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from bs4 import BeautifulSoup
from collections import deque
import time


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'product_urls_html_stream'
TRANSFORM_STREAM_NAME = 'transform_product_urls_html_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PAGINATION_STRING_IN_URL = 'pageindex'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
)
def scrape_product_urls_html_superseis():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return
    
    
    @task()
    def extract_category_urls():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = '''
            SELECT supermarket_id, distinct(url)
            FROM category_urls
            WHERE supermarket_id = 1
            ORDER BY created_at;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No category URLs found for Superseis in `category_urls` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        category_urls = []
        
        for row in results:
            category_urls.append({
                'supermarket_id': row[0],
                'url': row[1]
            })
        
        my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *category_urls)
        
        return


    @task()
    def transform_category_urls_to_product_urls_html():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=1, block_time_ms=5_000)        
        
            if batch is None:
                break
        
            category_url = batch[0]
        
            visited_urls = set()
            queue = deque([category_url['url']])

            product_urls_htmls = []

            while queue:
                time.sleep(0.5)
                visiting_url = queue.popleft()

                try:
                    response = requests.get(visiting_url, timeout=30)
                    response.raise_for_status()
                    html_content = response.text

                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    links = soup.find_all('a', href=True)

                    for link in links:
                        if (PAGINATION_STRING_IN_URL in link['href'].lower()) and (link['href'] not in visited_urls):
                            queue.append(link['href'])
                            visited_urls.add(link['href'])

                    product_urls_html = {
                        'supermarket_id': category_url['supermarket_id'],
                        'html': html_content,
                        'url': visiting_url,
                        'created_at': datetime.now().isoformat()
                    }

                    product_urls_htmls.append(product_urls_html)
                    
                except RequestException as e:
                    print(f'Failed to fetch URL {visiting_url}: {e}')

            my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[category_url['entry_id']])
            my_broker.write_pipeline(OUTPUT_STREAM_NAME, *product_urls_htmls)
        
        return


    setup = setup_transform_stream()
    extract = extract_category_urls()
    transform = transform_category_urls_to_product_urls_html()

    setup >> extract >> transform


scrape_product_urls_html_superseis()