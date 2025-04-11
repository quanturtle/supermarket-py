# Supermarket.py
A project that scrapes data from paraguayan supermarkets.

## Architecture
* Frontend (`next.js`)
* Backend (`fastapi`)
* DB (`postgres`)
* Pipeline (`mage.ai`)

## Screenshots

![](./img/home.png)

![](./img/catalog.png)

![](./img/inflation.png)

![](./img/cart.png)


## Install
Make sure `run_app.sh` is executable:
```sh
chmod +x run_app.sh
```

Use [`neon`](https://neon.tech/) as a `postgres` database. Create an account and use connection string:
```
postgresql://my_user:my_password@***-pooler.us-east-2.aws.neon.tech/my_database?sslmode=require
```

Modify `.env` file:
```
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_DB='supermarket'

BACKEND_PORT='8000'

MAGE_DATA_DIR='/app'
LOCAL_MAGE_DATA_DIR='/home/user/your/directory'
PIPELINE_HOST='localhost'
PIPELINE_PORT='6789'
```

Build and run with `docker`:
```sh
docker compose build && docker compose up
```