'''
DAG: config_streams_init
Create Redis streams
'''
import broker
from airflow.decorators import dag, task


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "retries": 0,
}

REDIS_CONN_ID = 'my-redis'


@dag(
    default_args=DEFAULT_ARGS,
    tags=["config"],
    catchup=False,
)
def config_streams_init():
    @task()
    def create_transform_streams():
        transform_streams = [
            'biggie_transform_category_urls_html_stream',
            'biggie_transform_category_urls_stream',
            'biggie_transform_product_urls_html_stream',
            'biggie_transform_product_urls_stream',
            'biggie_transform_products_html_stream',
            'biggie_transform_products_stream',
            'casarica_transform_category_urls_html_stream',
            'casarica_transform_category_urls_stream',
            'casarica_transform_product_urls_html_stream',
            'casarica_transform_product_urls_stream',
            'casarica_transform_products_html_stream',
            'casarica_transform_products_stream',
            'superseis_transform_category_urls_html_stream',
            'superseis_transform_category_urls_stream',
            'superseis_transform_product_urls_html_stream',
            'superseis_transform_product_urls_stream',
            'superseis_transform_products_html_stream',
            'superseis_transform_products_stream'
        ]

        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        GROUP_NAME = 'product_db_inserters'

        for transform_stream_name in transform_streams:
            my_broker.create_xgroup(transform_stream_name, GROUP_NAME)

        return


    @task()
    def create_output_streams():
        output_streams = [
            'category_urls_html_stream',
            'category_urls_stream',
            'product_urls_html_stream',
            'product_urls_stream',
            'products_html_stream',
            'products_stream'
        ]
        
        my_broker = broker.Broker(redis_connection_id=REDIS_CONN_ID)
        my_broker.create_connection()

        GROUP_NAME = 'product_db_inserters'

        for output_stream_name in output_streams:
            my_broker.create_xgroup(output_stream_name, GROUP_NAME)

        return


    (
        create_transform_streams()
        >> create_output_streams()
    )


config_streams_init()