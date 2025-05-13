'''
# parametrized_casarica_products
PRODUCTS_HTML --> PRODUCTS
'''
import broker
from constants import *
from datetime import datetime
from bs4 import BeautifulSoup
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'

OUTPUT_STREAM_NAME = 'products_stream'
TRANSFORM_STREAM_NAME = 'casarica_transform_products_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_products'
SUPERMARKET_ID = SupermarketID.CASA_RICA.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_CONTAINER_TAG = 'div'
PRODUCT_CONTAINER_CLASS = 'single-product-wrapper'

PRODUCT_NAME_TAG = 'h1'
PRODUCT_NAME_CLASS = 'product_title entry-title'

PRODUCT_SKU_TAG = 'span'
PRODUCT_SKU_CLASS = 'sku'
PRODUCT_SKU_ATTRS = {'id': 'producto-codigo'}

PRODUCT_PRICE_TAG = ['p', 'span']
PRODUCT_PRICE_CLASS = ['price', 'ecommercepro-Price-amount amount']
PRODUCT_PRICE_ATTRS = [{}, {'id': 'producto-precio'}]


@dag(
    default_args=DEFAULT_ARGS,
    tags=['casarica', 'parametrized'],
    catchup=False,
    doc_md=__doc__
)
def parametrized_casarica_scrape_products():
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

                for product_html in batch:
                    soup = BeautifulSoup(product_html['html'], 'html.parser')
                    
                    product_details_container = soup.find(PRODUCT_CONTAINER_TAG, class_=PRODUCT_CONTAINER_CLASS)
                    
                    if not product_details_container:
                        product = {
                            'supermarket_id': product_html['supermarket_id'],
                            'description': '',
                            'sku': '',
                            'price': '',
                            'url': product_html['url'],
                            'created_at': datetime.now().isoformat()
                        }
                        
                        my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_html['entry_id']])
                        my_broker.write(OUTPUT_STREAM_NAME, product)
                    
                        continue

                    try:        
                        product_description = product_details_container.find(
                            PRODUCT_NAME_TAG, class_=PRODUCT_NAME_CLASS
                        ).text.strip().upper()
                    
                    except:
                        product_description = ''

                    try:
                        product_sku = product_details_container.find(
                            PRODUCT_SKU_TAG, class_=PRODUCT_SKU_CLASS, attrs=PRODUCT_SKU_ATTRS
                        ).text.strip()
                        product_sku = ''.join(filter(str.isdigit, product_sku))
                    
                    except:
                        product_sku = ''

                    try:
                        product_price_container = product_details_container.find(
                            PRODUCT_PRICE_TAG[0], class_=PRODUCT_PRICE_CLASS[0], attrs=PRODUCT_PRICE_ATTRS[0]
                        )
                        
                        if product_price_container:
                            product_price_span = product_price_container.find(
                                PRODUCT_PRICE_TAG[1], class_=PRODUCT_PRICE_CLASS[1]
                            ).text.strip()
                            product_price = ''.join(filter(str.isdigit, product_price_span))
                            product_price = int(product_price) if product_price else 0
                        
                        else:
                            product_price = 0
                    
                    except:
                        product_price = 0
                    
                    product = {
                        'supermarket_id': product_html['supermarket_id'],
                        'description': product_description,
                        'sku': product_sku,
                        'price': product_price,
                        'url': product_html['url'],
                        'created_at': datetime.now().isoformat()
                    }

                    # load
                    my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[product_html['entry_id']])
                    my_broker.write(OUTPUT_STREAM_NAME, product)
        
        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [TRANSFORM]')
            print(e)
                
        return

 
    transform = transform_products_html_to_products(worker_id=PARALLEL_WORKERS)

    transform


parametrized_casarica_scrape_products()