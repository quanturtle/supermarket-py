# producer.py
import os
import json
import logging
from dotenv import load_dotenv
from redis import Redis
from rq import Queue

# Configure basic logging for the producer script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Environment Variables
load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or None
REDIS_DB = int(os.getenv('REDIS_DB', 0))
RQ_QUEUE_NAME = os.getenv('RQ_QUEUE_NAME', 'default')

# Sample product data
product = {
    "id": f"PROD{hash(os.times()) % 10000}", # Generate a somewhat unique ID
    "name": "Refactored Widget",
    "price": 25.50,
    "description": "A widget enqueued via the refactored producer.",
    "category": "Refactored",
    "stock": 50
}

# Convert product data to JSON string
product_json = json.dumps(product)

if __name__ == "__main__":
    logging.info(f"Connecting to Redis: {REDIS_HOST}:{REDIS_PORT}")
    try:
        # Producer doesn't need decode_responses typically
        redis_conn = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )
        redis_conn.ping() # Test connection
        logging.info("Redis connection successful.")
    except Exception as e:
        logging.error(f"Error connecting to Redis: {e}", exc_info=True)
        exit(1)

    # Get the queue
    q = Queue(RQ_QUEUE_NAME, connection=redis_conn)

    # Enqueue the job
    # IMPORTANT: The function path MUST now point to the function in consumer.py
    function_path = 'consumer.process_product_message'
    try:
        job = q.enqueue(
            function_path,
            product_json  # Argument for the function
        )
        logging.info(f"Enqueued job {job.id} to queue '{RQ_QUEUE_NAME}' targeting function '{function_path}'")
        logging.info(f"Job data: {product_json}")
    except Exception as e:
         logging.error(f"Failed to enqueue job: {e}", exc_info=True)