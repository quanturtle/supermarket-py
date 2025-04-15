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
postgresql://my_user:my_password@***-***.us-east-2.aws.neon.tech/my_database?sslmode=require
```

Deploy frontend to [`vercel`](http://vercel.com/) and get `FRONTEND_URL`.

Modify `.env` file:
```
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_DB='supermarket'

BACKEND_PORT='8000'
FRONTEND_URL='something.com'

MAGE_DATA_DIR='/app'
LOCAL_MAGE_DATA_DIR='/home/user/your/directory'
PIPELINE_HOST='localhost'
PIPELINE_PORT='6789'
```

Build and run with `docker`:
> [!NOTE]  
> Make sure to have the correct `.env` file when running docker compose
> `docker compose -env_file ./env.dev -f [...]` won't work because it won't perform substitution at compose time

```sh
# local development
docker compose -f docker-compose-dev.yaml build && docker compose -f docker-compose-dev.yaml up
```

```sh
# production deployment
docker compose -f docker-compose-prod.yaml build && docker compose -f docker-compose-prod.yaml up
```

TODO:
New URLs:
* https://supermercadolabomba.com/index.php?class=Inicio
* https://losjardinesonline.com.py/
* https://www.supermas.com.py/
* https://kingo.com.py/index.php?class=Inicio
* https://www.fortis.com.py/
* https://grutteronline.casagrutter.com.py/
* https://www.salemmaonline.com.py/

* Biggie
    * Build category and product url extraction pipeline
    * Build product extraction pipeline

* Standarize URLs (https://www.supermas.com.py/)
    * https://
    * www.
    * .com.py/

* Add column to `supermarket` to hold another column: `pagination_container`
    * Add next pagination url class/url selector

* Standarize price extraction in case there is a discount and the new price shows up next to the old price

* Make backup selection process (CSS selector vs class based selection)    
    * Compare result of CSS selector and class based selector to make sure we got the correct data from the page