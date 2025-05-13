'''
# parametrized_biggie_product_urls
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
import re
import unicodedata
from datetime import datetime
import json
import broker
from constants import *
from airflow.decorators import dag, task
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
SUPERMARKET_ID = SupermarketID.BIGGIE.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'parametrized'],
    catchup=False,
    doc_md=__doc__
)
def parametrized_biggie_scrape_product_urls():
    def create_url_suffix(name, code):
        name = str(name).replace('‘', "'").replace('´', '').replace('#', '').replace('(', '').replace(')', '').replace('?', '')
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
        name = re.sub(r'[./%]', '', name)
        slug = re.sub(r'\s+', '-', name).strip('-')

        return f'{slug}-{code}'


    @task()
    def transform_product_urls_html_to_product_urls(worker_id: int, **context):
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        run_id = context['dag_run'].run_id
        task_instance = context['ti'].dag_id

        worker_name = f"{CONSUMER_NAME}-{run_id}-{task_instance}-{worker_id}".replace('.', '_').replace(':','-')

        try:
            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, worker_name, batch_size=WORKER_BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
            
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

                        product_urls.append(product_url)

                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url_html['entry_id']])
                    my_broker.write_pipeline(OUTPUT_STREAM_NAME, *product_urls)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)

        return

    
    transform = transform_product_urls_html_to_product_urls(worker_id=PARALLEL_WORKERS)

    transform


parametrized_biggie_scrape_product_urls()