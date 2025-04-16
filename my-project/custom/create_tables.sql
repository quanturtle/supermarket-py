CREATE TABLE IF NOT EXISTS supermarkets (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR,
    home_url VARCHAR,
    category_urls_container_url VARCHAR,
    category_urls_container_class VARCHAR,
    api_url VARCHAR
);

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

CREATE TABLE IF NOT EXISTS category_urls (
    id SERIAL PRIMARY KEY,
    supermarket_id INT REFERENCES supermarkets (id),
    description VARCHAR,
    url VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_urls (
    id SERIAL PRIMARY KEY,
    supermarket_id INT REFERENCES supermarkets (id),
    description VARCHAR,
    url VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    supermarket_id INT REFERENCES supermarkets (id),
    description VARCHAR,
    sku VARCHAR,
	price DECIMAL,
    url VARCHAR,
	created_at TIMESTAMP
);