CREATE TABLE IF NOT EXISTS supermarkets (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR,
    home_url VARCHAR,
    category_urls_container_url VARCHAR,
    api_url VARCHAR
);

CREATE TABLE IF NOT EXISTS category_urls (
    id SERIAL PRIMARY KEY,
    supermarket_id integer REFERENCES supermarkets (id),
    description VARCHAR,
    url VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    supermarket_id integer REFERENCES supermarkets (id),
    "name" VARCHAR,
    sku VARCHAR,
	price DECIMAL,
	created_at TIMESTAMP
);