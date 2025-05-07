'''
DAG: database_init
Create tables
'''
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "retries": 0,
}

POSTGRES_CONN_ID = "my-db"


def _run_sql(sql: str) -> None:
    PostgresHook(postgres_conn_id=POSTGRES_CONN_ID).run(sql)


@dag(
    default_args=DEFAULT_ARGS,
    tags=["config"],
    catchup=False,
)
def database_init():
    @task()
    def create_supermarkets():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS supermarkets (
                id SERIAL PRIMARY KEY,
                "name" VARCHAR,
                home_url VARCHAR,
                category_urls_container_url VARCHAR,
                category_urls_container_class VARCHAR,
                api_url VARCHAR
            );
        """)


    @task()
    def create_supermarket_configs():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS supermarket_configs (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                category_urls_container_url VARCHAR,
                category_string_in_url VARCHAR,
                product_string_in_url VARCHAR,
                pagination_string_in_url VARCHAR,
                product_container_tag VARCHAR,
                product_container_class VARCHAR,
                product_container_attrs VARCHAR,
                product_container_name_tag VARCHAR,
                product_container_name_class VARCHAR,
                product_container_name_attrs VARCHAR,
                product_container_price_tag VARCHAR,
                product_container_price_class VARCHAR,
                product_container_price_attrs VARCHAR,
                product_container_sku_tag VARCHAR,
                product_container_sku_class VARCHAR,
                product_container_sku_attrs VARCHAR
            );
        """)


    @task()
    def create_category_urls_html():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS category_urls_html (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                html TEXT,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def create_category_urls():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS category_urls (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                description VARCHAR,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def create_product_urls_html():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS product_urls_html (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                html TEXT,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def create_product_urls():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS product_urls (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                description VARCHAR,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def create_products_html():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS products_html (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                html TEXT,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def create_products():
        _run_sql("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                supermarket_id INT REFERENCES supermarkets (id),
                description VARCHAR,
                sku VARCHAR,
                price DECIMAL,
                url VARCHAR,
                created_at TIMESTAMP
            );
        """)


    @task()
    def seed_supermarkets():
        _run_sql("""
            INSERT INTO supermarkets (id, "name", home_url, category_urls_container_url, category_urls_container_class, api_url)
            VALUES
                (1, 'Superseis', 'http://superseis.com.py/', 'http://superseis.com.py/', 'col-header header-categorias hidden-xs', ''),
                (2, 'Stock', 'https://www.stock.com.py/', 'https://www.stock.com.py/', 'col-header header-categorias hidden-xs', ''),
                (3, 'Biggie', 'https://biggie.com.py/', '', '', 'https://api.app.biggie.com.py/api/classifications/web?take=-1&storeType='),
                (4, 'Arete', 'https://www.arete.com.py/', 'https://www.arete.com.py/', 'dropdown-menu yamm departments-menu-dropdown', ''),
                (5, 'Casa_rica', 'https://casarica.com.py/', 'https://casarica.com.py/', 'dropdown-menu yamm departments-menu-dropdown', ''),
                (6, 'Fortis', 'https://www.fortis.com.py/', 'https://www.fortis.com.py/', 'hero__list border', '')
            ON CONFLICT (id) DO NOTHING;
        """)


    (
        create_supermarkets()
        >> create_supermarket_configs()
        >> create_category_urls_html()
        >> create_category_urls()
        >> create_product_urls_html()
        >> create_product_urls()
        >> create_products_html()
        >> create_products()
        >> seed_supermarkets()
    )


database_init()