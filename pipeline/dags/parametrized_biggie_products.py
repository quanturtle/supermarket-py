'''
# parametrized_biggie_products
PRODUCTS_HTML --> PRODUCTS

this is a special case, the API response from product_urls_html is enough to populate the products table
'''
import json
import broker
from datetime import datetime
from constants import *
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'products_stream'
TRANSFORM_STREAM_NAME = 'biggie_transform_products_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_products'
SUPERMARKET_ID = SupermarketID.BIGGIE.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_NAME = 'name'
PRODUCT_SKU = 'code'
PRODUCT_PRICE = 'price'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'parametrized'],
    catchup=False,
    doc_md=__doc__
)
def parametrized_biggie_scrape_products():
    @task()
    def transform_products_html_to_products(worker_id: int, **context):
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

                for product_htmls in batch:
                    products = []
                    products_json = json.loads(product_htmls['html'])
                    
                    for item in products_json:
                        url_suffix = item['name'].replace('.', '') \
                                    .replace(' ', '-') \
                                    .replace('´', '') \
                                    .replace('‘', '\'') \
                                    .lower() + '-' + item['code']
                        
                        product = {
                            'supermarket_id': product_htmls['supermarket_id'],
                            'description': item['name'].upper(),
                            'sku': item['code'],
                            'price': item['price'],
                            'url': f'https://biggie.com.py/item/{url_suffix}',
                            'created_at': datetime.now().isoformat()
                        }

                        products.append(product)
                
                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_htmls['entry_id']])
                    my_broker.write_pipeline(OUTPUT_STREAM_NAME, *products)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)

        return


    transform = transform_products_html_to_products.expand(worker_id=PARALLEL_WORKERS)

    transform


parametrized_biggie_scrape_products()