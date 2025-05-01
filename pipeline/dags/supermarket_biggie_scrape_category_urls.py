'''
DAG: supermarket_biggie_scrape_category_urls
SUPERMARKETS --> CATEGORY_URLS_HTML
'''
from datetime import datetime
import json
import broker
from requests.exceptions import RequestException
from redis.exceptions import ResponseError
from airflow.decorators import dag, task
from airflow.exceptions import AirflowNotFoundException
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'retries': 0,
}

POSTGRES_CONN_ID = 'my-db'
REDIS_CONN_ID = 'my-redis'
OUTPUT_STREAM_NAME = 'category_urls_stream'
TRANSFORM_STREAM_NAME = 'biggie_transform_category_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

SUPERMARKET_ID = 3
BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

@dag(
    default_args=DEFAULT_ARGS,
    tags=['biggie', 'etl'],
    catchup=False,
)
def supermarket_biggie_scrape_category_urls():
    @task()
    def setup_transform_stream():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        my_broker.create_xgroup(TRANSFORM_STREAM_NAME, GROUP_NAME)

        return
    
    @task()
    def extract_category_urls_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        sql = f'''
            SELECT supermarket_id, html, url
            FROM category_urls_html
            WHERE supermarket_id = {SUPERMARKET_ID}
            ORDER BY created_at;
        '''

        result = hook.get_first(sql)

        if not result:
            raise AirflowNotFoundException('No Biggie row found in `supermarkets` table.')

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        my_broker.write(TRANSFORM_STREAM_NAME, {
            'supermarket_id': result[0], 
            'html': result[1], 
            'url': result[2]
        })

        return


    @task()
    def transform_category_urls_html_to_category_urls():
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        while True:
            batch = my_broker.read(TRANSFORM_STREAM_NAME, GROUP_NAME, CONSUMER_NAME, batch_size=BATCH_SIZE, block_time_ms=BLOCK_TIME_MS)        
        
            if batch is None:
                break
        
            for category_urls_html in batch:
                try:
                    api_response = json.loads(category_urls_html['html'])
                    api_items = api_response['items']
                except:
                    print('Error loading json from supermarkets')

                category_urls = []
                
                LIMIT = 50
                OFFSET = 0

                for item in api_items:
                    slug = item['slug'].strip()
                    url_with_slug = f'https://api.app.biggie.com.py/api/articles?take={LIMIT}&skip={OFFSET}&classificationName={slug}'

                    category_url = {
                        'supermarket_id': category_urls_html['supermarket_id'],
                        'description': item['name'],
                        'url': url_with_slug,
                        'created_at': datetime.now().isoformat()
                    }
                
                    category_urls.append(category_url)

                my_broker.ack(TRANSFORM_STREAM_NAME, GROUP_NAME, *[category_urls_html['entry_id']])
                my_broker.write_pipeline(OUTPUT_STREAM_NAME, *category_urls)
        
        return


    setup = setup_transform_stream()
    extract = extract_category_urls_html()
    transform = transform_category_urls_html_to_category_urls()

    setup >> extract >> transform


supermarket_biggie_scrape_category_urls()