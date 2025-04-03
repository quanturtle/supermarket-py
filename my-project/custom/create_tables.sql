CREATE TABLE IF NOT EXISTS supermarkets (
    "name" VARCHAR,
    home_url VARCHAR,
    categories_container VARCHAR
);

CREATE TABLE IF NOT EXISTS urls (
    url VARCHAR,
    created_at TIMESTAMP,
    last_visited TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
	"name" VARCHAR,
    sku VARCHAR,
	price VARCHAR,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
);