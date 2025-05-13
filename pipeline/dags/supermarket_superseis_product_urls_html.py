'''
# supermarket_superseis_product_urls_html
CATEGORY_URLS --> PRODUCT_URLS_HTML
'''
import time
import broker
import requests
from constants import *
from bs4 import BeautifulSoup
from datetime import datetime
from collections import deque
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'product_urls_html_stream'
TRANSFORM_STREAM_NAME = 'superseis_transform_product_urls_html_stream'
ERROR_REQUEST_STREAM_NAME = 'error_request_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls_html'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value

PARALLEL_WORKERS = list(range(9))
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000
DELAY_SECONDS = 0.5

PAGINATION_STRING_IN_URL = 'pageindex'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
    doc_md=__doc__
)
def supermarket_superseis_product_urls_html():
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
    def transform_category_urls_to_product_urls_html(worker_id: int, **context):
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        run_id = context['dag_run'].run_id
        task_instance = context['ti'].dag_id

        worker_name = f'{CONSUMER_NAME}-{run_id}-{task_instance}-{worker_id}'.replace('.', '_').replace(':','-')

        try:
            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, worker_name, batch_size=WORKER_BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
            
                if batch is None:
                    break
            
                for category_url in batch:
                    visited_urls = {category_url["url"]}
                    queue = deque([category_url['url']])

                    product_urls_htmls = []

                    while queue:
                        time.sleep(DELAY_SECONDS)
                        visiting_url = queue.popleft()

                        try:
                            response = requests.get(visiting_url, timeout=30)
                            html_content = response.text

                        except Exception as e:
                            print(e)
                            my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': visiting_url, 'detail': str(e)})
                            continue

                        else:
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

                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[category_url['entry_id']])
                    my_broker.write_pipeline(OUTPUT_STREAM_NAME, *product_urls_htmls)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)
        
        return


    setup = setup_transform_stream()
    extract = extract_category_urls()
    transform = transform_category_urls_to_product_urls_html.expand(worker_id=PARALLEL_WORKERS)

    setup >> extract >> transform


supermarket_superseis_product_urls_html()