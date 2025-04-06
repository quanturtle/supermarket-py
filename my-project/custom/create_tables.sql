CREATE TABLE IF NOT EXISTS supermarkets (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR,
    home_url VARCHAR,
    categories_container_url VARCHAR,
    categories_container VARCHAR
);

CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR,
    created_at TIMESTAMP,
    last_visited TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR,
    sku VARCHAR,
	price VARCHAR,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category_urls (
    id SERIAL PRIMARY KEY,
    supermarket_id integer REFERENCES supermarkets (id),
    description VARCHAR,
    url VARCHAR
);