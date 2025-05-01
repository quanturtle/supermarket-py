'''
DAG: supermarket_superseis_scrape_products
PRODUCTS_HTML --> PRODUCTS
'''
import broker
from datetime import datetime
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from bs4 import BeautifulSoup


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'products_stream'
TRANSFORM_STREAM_NAME = 'transform_products_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

SUPERMARKET_ID = 1

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
)
def supermarket_superseis_scrape_products():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return
    

    @task()
    def extract_products_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = f'''
            SELECT supermarket_id, html, url
            FROM products_html
            WHERE supermarket_id = {SUPERMARKET_ID}
            ORDER BY created_at;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No product HTML content found for Superseis in `products_html` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        products_htmls = []
        
        for row in results:
            products_htmls.append({
                'supermarket_id': row[0],
                'html': row[1],
                'url': row[2]
            })

        my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *products_htmls)
        
        return


    @task()
    def transform_products_html_to_products():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=20, block_time_ms=5_000)        
        
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
                        product_price = None
                
                except:
                    product_price = None
                
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
                
        return


    setup = setup_transform_stream()
    extract = extract_products_html()    
    transform = transform_products_html_to_products()

    setup >> extract >> transform


supermarket_superseis_scrape_products()