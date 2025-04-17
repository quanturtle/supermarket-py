ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "main.py"]