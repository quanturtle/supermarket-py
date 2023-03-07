# supermarket-py
A project that scrapes price data from paraguayan supermarkets

## Motivation and Objective


## Structure

```
├── README.md
├── backend
├── docker-compose.yml
├── linkgenerator
└── product_scraper
```

`backend`: a `django-rest` API for storing all of the information
`linkgenerator`: simple `requests` scripts that extract all links from supermarkets landing pages, stores urls in the `backend`
`product_scraper`: a `scrapy` project that has spiders that retrieves all urls stored in `backend` and finds all products in the supermarket website

## Running the project
WIP  
Eventually the project should be run using `docker compose`

## TO DO
* Add frontend
* Add `postgres`
* Add `Dockerfiles` to every service
* Add `docker-compose` file