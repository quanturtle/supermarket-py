ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  

# Copy only requirements.txt to the container
COPY requirements.txt /app/

# Install dependencies and clean up cache
RUN set -ex && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /root/.cache/

# Copy the rest of the application files into the container
COPY . /app/

# Expose the port for the app
EXPOSE 8000

# Define the default command
CMD ["fastapi", "run", "main.py", "--port", "8000"]