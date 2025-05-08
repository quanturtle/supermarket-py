'''
DAG: supermarket_biggie_scrape_products
PRODUCTS_HTML --> PRODUCTS

this is a special case, the API response from product_urls_html is enough to populate the products table
'''
import json
import broker
from datetime import datetime
from constants import *
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
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
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_NAME = 'name'
PRODUCT_SKU = 'code'
PRODUCT_PRICE = 'price'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def supermarket_biggie_scrape_products():
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
            FROM product_urls_html
            WHERE supermarket_id = {SUPERMARKET_ID}
            ORDER BY created_at;
        '''

        results = hook.get_records(sql)

        if not results:
            raise AirflowNotFoundException('No product HTML content found for biggie in `products_html` table.')

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
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
        
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
                
        return


    setup = setup_transform_stream()
    extract = extract_products_html()    
    transform = transform_products_html_to_products()

    setup >> extract >> transform


supermarket_biggie_scrape_products()