# supermarket-py
A project that scrapes price data from paraguayan supermarkets

## Motivation and Objective
Create a dataset of products stocked in paraguayan supermarkets, make it easily accessible for anyone to download and make use of technologies I have recently learned. 

## Structure

```
├── README.md
├── backend
├── docker-compose.yml
├── linkgenerator
└── product_scraper
```

`backend`: a `django-rest` API for storing all of the information  
`linkgenerator`: simple `requests` scripts that extracts all links from supermarkets' landing pages, stores urls in the `backend`  
`product_scraper`: a `scrapy` project that has spiders that retrieve all urls stored in `backend` and finds all products in the supermarket website  

## Running the project
You should be able to run every component of the project by running the following command inside the component directory:
```
docker build -t <component_name> .
```
_Note: Remember to create the .env from .env.sample file in the backend directory before building_

Run Django+Postgres:
```
docker compose up --build
```

## TO DO
* Add logs
* Add frontend
* Add `Dockerfile` to every service
  * `linkgenerator`
  * `product_scraper`
* Add rest of services to `docker-compose` file
  * `linkgenerator`
  * `product_scraper`