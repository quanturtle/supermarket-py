FROM python:3.8-slim

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD django

# set the working directory
WORKDIR /app

# copy the requirements file and install dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code
COPY . .

# expose the port
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
# start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]