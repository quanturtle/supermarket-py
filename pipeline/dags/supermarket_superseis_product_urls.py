'''
# supermarket_superseis_product_urls
PRODUCT_URLS_HTML --> PRODUCT_URLS
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

OUTPUT_STREAM_NAME = 'product_urls_stream'
TRANSFORM_STREAM_NAME = 'superseis_transform_product_urls_stream'
GROUP_NAME = 'product_db_inserters'
CONSUMER_NAME = 'transformer'

PIPELINE_NAME = 'scrape_product_urls'
SUPERMARKET_ID = SupermarketID.SUPERSEIS.value

PARALLEL_WORKERS = list(range(9))
CURSOR_BATCH_SIZE = 100
WORKER_BATCH_SIZE = 20
BLOCK_TIME_MS = 1_000

PRODUCT_STRING_IN_URL = 'products'


@dag(
    default_args=DEFAULT_ARGS,
    tags=['superseis', 'etl'],
    catchup=False,
    doc_md=__doc__
)
def supermarket_superseis_product_urls():
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
    def extract_product_urls_html():
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()
        
        try:
            with hook.get_conn() as conn, conn.cursor(name="products_cursor") as cur:
                cur.itersize = CURSOR_BATCH_SIZE
                cur.execute(
                    '''
                    SELECT supermarket_id, html, url
                    FROM product_urls_html
                    WHERE supermarket_id = %s
                    ORDER BY created_at;
                    ''',
                    (SUPERMARKET_ID,),
                )

                while True:
                    rows = cur.fetchmany(CURSOR_BATCH_SIZE)
                    
                    if not rows:
                        break

                    product_urls_html = [
                        {'supermarket_id': row[0], 'html': row[1], 'url': row[2]}
                        for row in rows
                    ]
                    
                    my_broker.write_pipeline(TRANSFORM_STREAM_NAME, *product_urls_html)

        except Exception as e:
            print(f'[{SUPERMARKET_ID}] - [{PIPELINE_NAME}] - [EXTRACT]')
            print(e)

        return


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

                    links = soup.find_all('a', href=True)

                    product_urls = []

                    for link in links:
                        if (PRODUCT_STRING_IN_URL in link['href'].lower()) and (link.get_text(strip=True) != ''):
                            product_url = {
                                'supermarket_id': product_url_html['supermarket_id'],
                                'description': link.get_text(strip=True),
                                'url': link['href'],
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

    
    setup = setup_transform_stream()
    extract = extract_product_urls_html()
    transform = transform_product_urls_html_to_product_urls.expand(worker_id=PARALLEL_WORKERS)

    setup >> extract >> transform


supermarket_superseis_product_urls()