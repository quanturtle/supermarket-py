'''
# parametrized_casarica_product_urls
PRODUCT_URLS_HTML --> PRODUCT_URLS
'''
import broker
from constants import *
from bs4 import BeautifulSoup
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'product_urls_stream'
TRANSFORM_STREAM_NAME = 'casarica_transform_product_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls'
SUPERMARKET_ID = SupermarketID.CASA_RICA.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_CONTAINER_TAG = 'div'
PRODUCT_CONTAINER_CLASS = 'tab-content'

DESCRIPTION_TAG = 'h2'
DESCRIPTION_CLASS = 'ecommercepro-loop-product__title'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['casarica', 'parametrized'],
    catchup=False,
    doc_md=__doc__
)
def parametrized_casarica_scrape_product_urls():
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
                    soup = BeautifulSoup(product_url_html['html'], 'html.parser')
                    product_div = soup.find(PRODUCT_CONTAINER_TAG, class_=PRODUCT_CONTAINER_CLASS)
                    
                    links = product_div.find_all('a', href=True)

                    product_urls = []

                    for link in links:
                        if link['href'] not in ['javascript:void(0);', 'mi-lista']:
                            description = link.find(DESCRIPTION_TAG, class_=DESCRIPTION_CLASS)
                            product_url = {
                                'supermarket_id': product_url_html['supermarket_id'],
                                'description': description.get_text(strip=True) if description else '',
                                'url': f'https://www.casarica.com.py/{link['href']}',
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

    
    transform = transform_product_urls_html_to_product_urls.expand(worker_id=PARALLEL_WORKERS)

    transform


parametrized_casarica_scrape_product_urls()