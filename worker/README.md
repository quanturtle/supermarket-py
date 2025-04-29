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

## Standalone build
```sh
docker build -t my-worker ./worker 
```

```sh
docker run -d --name my-worker \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=postgres \
  -e REDIS_HOST=host.docker.internal \
  -e REDIS_PORT=6379 \
  -e BATCH_SIZE=100 \
  -e BATCH_TIME_LIMIT=10 \
  -p 6380:6380 \
  worker-airflow
```