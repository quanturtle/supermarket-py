import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from redis import Redis
from rq import Queue
import consumer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
RQ_QUEUE_NAME = os.getenv("RQ_QUEUE_NAME", "default")


if __name__ == "__main__":
    product = {
        "supermarket_id": 1,
        "description": "Refactored Widget",
        "sku": f"WIDGET-{hash(os.times()) % 10000}",
        "price": 25.50,
        "url": "hello.com"
        # omit created_at so SQLModel will default to now()
    }

    product_json = json.dumps(product)

    logging.info(f"Connecting to Redis: {REDIS_HOST}:{REDIS_PORT}")

    try:
        redis_conn = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB,
        )
        
        redis_conn.ping()
        logging.info("Redis connection successful.")
    
    except Exception as e:
        logging.error(f"Error connecting to Redis: {e}", exc_info=True)
        exit(1)

    q = Queue(RQ_QUEUE_NAME, connection=redis_conn)

    try:
        job = q.enqueue(consumer.process_product_message, product_json)
    
        logging.info(f"Enqueued job {job.id} → process_product_message")
        logging.debug(f"Payload: {product_json}")
    
    except Exception as e:
        logging.error(f"Failed to enqueue job: {e}", exc_info=True)