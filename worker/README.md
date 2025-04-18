# worker

## Run locally
Create `.env` file:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

POSTGRES_USER='postgres'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_DB='postgres'

LOG_LEVEL=INFO
IS_PROD='False'
```

Install packages:
```sh
uv sync # or pip install -r requirements.txt
```

Run `consumer`:
```sh
uv run main.py # or python main.py
```

Once the `consumer` is running, run the `producer`:
```sh
uv run producer.py --mode stream --count 500
uv run producer.py --mode bulk --count 500
```