'''
# parametrized_superseis_products_html
PRODUCT_URLS --> PRODUCTS_HTML
'''
import time
import broker
import requests
from constants import *
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'products_html_stream'
TRANSFORM_STREAM_NAME = 'superseis_transform_products_html_stream'
ERROR_REQUEST_STREAM_NAME = 'error_request_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_products_html'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value

PARALLEL_WORKERS = list(range(9))
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000
DELAY_SECONDS = 0.5


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'parametrized'],
    catchup=False,
    doc_md=__doc__
)
def parametrized_superseis_scrape_products_html():
    @task()
    def transform_product_urls_to_products_html(worker_id: int, **context):
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

                for product_url in batch:
                    try:
                        time.sleep(DELAY_SECONDS)
                        response = requests.get(product_url['url'], timeout=30)
                        html_content = response.text

                    except Exception as e:
                        print(e)
                        my_broker.write(ERROR_REQUEST_STREAM_NAME, {'url': product_url['url'], 'detail': str(e)})
                        continue
                    
                    else:
                        product_html = {
                            'supermarket_id': product_url['supermarket_id'],
                            'html': html_content,
                            'url': product_url['url'],
                            'created_at': datetime.now().isoformat()
                        }

                        # load
                        my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_url['entry_id']])
                        my_broker.write(OUTPUT_STREAM_NAME, product_html)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)
        
        return


    transform = transform_product_urls_to_products_html.expand(worker_id=PARALLEL_WORKERS)

    transform


parametrized_superseis_scrape_products_html()