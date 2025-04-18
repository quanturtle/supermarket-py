# backend

## Run locally
Create an `.env` file:
```
IS_PROD='False'
FRONTEND_URL='my_frontend.com'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_DB='postgres'
```
Install dependencies:
```sh
uv sync # or pip install -r requirements.txt
```

Run app:
```sh
uv run main.py # or python main.py
```
Test endpoints by running `postman` collection.