#!/bin/bash

# entrypoint.sh file of Dockerfile

# Section 1- Bash options
set -o errexit
set -o pipefail
set -o nounset

# Section 2: Health of dependent services
postgres_ready() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError
import config

cfg = config.Config('.env')

try:
    connect(
        dbname=cfg['SQL_DATABASE'],
        user=cfg['SQL_USER'],
        password=cfg['SQL_PASSWORD'],
        host=cfg['SQL_HOST'],
        port=cfg['SQL_PORT'],
    )
except OperationalError:
    sys.exit(-1)
END
}

until postgres_ready; do
  >&2 echo "Waiting for PostgreSQL to become available..."
  sleep 5
done
>&2 echo "PostgreSQL is available"

# Section 3- Idempotent Django commands
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py loaddata home/fixtures/supermarket.json --app home.supermarket

exec "$@"
