import os
import json
from dotenv import load_dotenv
from redis import Redis
from rq import Queue

# Load Environment Variables (same as consumer)
load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or None
REDIS_DB = int(os.getenv('REDIS_DB', 0))
RQ_QUEUE_NAME = os.getenv('RQ_QUEUE_NAME', 'default')

# Sample product data
product = {
    "id": "PROD12345",
    "name": "Example Widget",
    "price": 19.99,
    "description": "A fine example widget.",
    "category": "Widgets",
    "stock": 100
}

# Convert product data to JSON string
product_json = json.dumps(product)

if __name__ == "__main__":
    print(f"Connecting to Redis: {REDIS_HOST}:{REDIS_PORT}")
    try:
        redis_conn = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )
        redis_conn.ping() # Test connection
        print("Redis connection successful.")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        exit(1)

    # Get the queue
    q = Queue(RQ_QUEUE_NAME, connection=redis_conn)

    # Enqueue the job
    # The first argument is the *path* to the function the worker should execute.
    # The following arguments are passed to that function.
    job = q.enqueue(
        'main.process_product_message', # Path to the function in consumer.py
        product_json                      # Argument for the function
    )

    job = q.enqueue(
        'main.process_product_message', # Path to the function in consumer.py
        product_json                      # Argument for the function
    )

    print(f"Enqueued job {job.id} to queue '{RQ_QUEUE_NAME}' with data:")
    print(product_json)