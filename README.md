# Tender Pipeline
Pipeline with mage.ai

## Install
Make sure `run_app.sh` is executable:
```sh
chmod +x run_app.sh
```

Modify `.env` file:
```
POSTGRES_USER='user'
POSTGRES_PASSWORD='password'
POSTGRES_DB='postgres'
POSTGRES_PORT='5432'

MAGE_DATA_DIR= '/app'
LOCAL_MAGE_DATA_DIR='/home/user/your/directory'
PIPELINE_HOST='localhost'
PIPELINE_PORT='6789'
```

Build and run with `docker`:
```sh
docker compose build && docker compose up
```

> [!NOTE]  
> unify `postgres` credentials between `my-pipeline/io_config.yaml`, `docker-compose.yaml` and `.env`