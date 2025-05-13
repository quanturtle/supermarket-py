'''
# supermarket_superseis_products
PRODUCTS_HTML --> PRODUCTS
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

OUTPUT_STREAM_NAME = 'products_stream'
TRANSFORM_STREAM_NAME = 'superseis_transform_products_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_products'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_CONTAINER_TAG = 'div'
PRODUCT_CONTAINER_CLASS = 'product-details-info'

PRODUCT_NAME_TAG = 'h1'
PRODUCT_NAME_CLASS = 'productname'
PRODUCT_NAME_ATTRS = {'itemprop': 'name'}

PRODUCT_SKU_TAG = 'div'
PRODUCT_SKU_CLASS = 'sku'
PRODUCT_SKU_ATTRS = {'itemprop': 'sku'}

PRODUCT_PRICE_TAG = ['div', 'span']
PRODUCT_PRICE_CLASS = ['price', 'productPrice']
PRODUCT_PRICE_ATTRS = [{'itemprop': 'price'}, '']


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
    doc_md=__doc__
)
def supermarket_superseis_products():
    @task()
    def setup_transform_stream():
        try:
            my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
            my_broker.create_connection()
            
            my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [SETUP]')
            print(e)
            raise

        return
    

    @task()
    def extract_products_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        try:
            with hook.get_conn() as conn, conn.cursor(name="products_cursor") as cur:
                cur.itersize = CURSOR_BATCH_SIZE
                cur.execute(
                    '''
                    SELECT supermarket_id, html, url
                    FROM products_html
                    WHERE supermarket_id = %s
                    ORDER BY created_at
                    ''',
                    (SUPERMARKET_ID,),
                )

                while True:
                    rows = cur.fetchmany(CURSOR_BATCH_SIZE)
                    
                    if not rows:
                        break

                    products_htmls = [
                        {'supermarket_id': row[0], 'html': row[1], 'url': row[2]}
                        for row in rows
                    ]
                    
                    my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *products_htmls)

        except Exception as e:
            print(e)
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [EXTRACT]')
            raise
        
        return


    @task()
    def transform_products_html_to_products(worker_id: int, **context):
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        run_id = context['dag_run'].run_id
        task_instance = context['ti'].dag_id

        worker_name = f'{CONSUMER_NAME}-{run_id}-{task_instance}-{worker_id}'.replace('.', '_').replace(':','-')

        try:
            while True:
                batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=WORKER_BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
            
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
                            PRODUCT_NAME_TAG, class_=PRODUCT_NAME_CLASS, attrs=PRODUCT_NAME_ATTRS
                        ).text.strip().upper()
                    
                    except:
                        product_description = product_html.get('description', '')

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


    setup = setup_transform_stream()
    extract = extract_products_html()    
    transform = transform_products_html_to_products.expand(worker_id=PARALLEL_WORKERS)

    setup >> extract >> transform


supermarket_superseis_products()