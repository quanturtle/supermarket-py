import os
import logging
import json
import time # For potential delays or simulations

from dotenv import load_dotenv
from redis import Redis, exceptions as redis_exceptions
from rq import Queue, Worker

# --- Load Environment Variables ---
load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or None # Handles empty string
REDIS_DB = int(os.getenv('REDIS_DB', 0))
RQ_QUEUE_NAME = os.getenv('RQ_QUEUE_NAME', 'default') # Default queue name

POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# --- Configure Logging ---
log_level_int = getattr(logging, LOG_LEVEL, logging.INFO)
logging.basicConfig(
    level=log_level_int,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# Silence noisy libraries if needed
logging.getLogger("rq.worker").setLevel(logging.WARNING)


# --- Placeholder Database Functions ---
def get_db_connection():
    """
    Placeholder function to establish a PostgreSQL connection.
    Replace with actual psycopg2 or other DB library connection logic.
    """
    logger.info("Attempting to connect to PostgreSQL (Placeholder)...")
    if not all([POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT]):
        logger.error("Database configuration missing in environment variables.")
        return None
    try:
        # --- Replace with actual connection ---
        # import psycopg2
        # conn = psycopg2.connect(
        #     dbname=POSTGRES_DBNAME,
        #     user=POSTGRES_USER,
        #     password=POSTGRES_PASSWORD,
        #     host=POSTGRES_HOST,
        #     port=POSTGRES_PORT
        # )
        # logger.info("Database connection successful (Simulated).")
        # return conn # Return the actual connection object
        # --- End Replace ---

        # Simulate connection attempt
        time.sleep(0.1)
        logger.info("Placeholder: Simulated database connection successful.")
        # Return a dummy object or None for the placeholder
        return {"dummy_connection": True} # Or simply None if preferred

    except Exception as e: # Catch specific DB errors in real implementation
        logger.error(f"Placeholder: Failed to connect to database: {e}", exc_info=True)
        return None

def insert_product_to_db(product_data, connection):
    """
    Placeholder function to insert product data into the database.
    Replace with actual database insertion logic using the connection.
    """
    logger.info(f"Attempting to insert product (Placeholder): {product_data.get('id', 'N/A')}")
    if connection is None:
        logger.error("Cannot insert product, database connection is invalid.")
        return False

    try:
        # --- Replace with actual insertion ---
        # with connection.cursor() as cursor:
        #     # Example: Adjust table_name and columns as needed
        #     sql = """
        #         INSERT INTO products (product_id, name, price, description, received_at)
        #         VALUES (%s, %s, %s, %s, NOW())
        #         ON CONFLICT (product_id) DO UPDATE SET
        #             name = EXCLUDED.name,
        #             price = EXCLUDED.price,
        #             description = EXCLUDED.description,
        #             received_at = NOW();
        #     """
        #     cursor.execute(sql, (
        #         product_data.get('id'),
        #         product_data.get('name'),
        #         product_data.get('price'),
        #         product_data.get('description')
        #     ))
        # connection.commit() # Commit the transaction
        # logger.info(f"Successfully inserted/updated product (Simulated): {product_data.get('id', 'N/A')}")
        # return True
        # --- End Replace ---

        # Simulate database work
        time.sleep(0.2)
        logger.info(f"Placeholder: Simulated insertion successful for product: {product_data.get('id', 'N/A')}")
        return True # Simulate success

    except Exception as e: # Catch specific DB errors
        logger.error(f"Placeholder: Failed to insert product data: {e}", exc_info=True)
        # if connection: # Rollback in real implementation
        #    connection.rollback()
        return False
    # finally:
        # Decide connection closing strategy:
        # - If pooling: Release connection back to pool
        # - If single connection per task: Close here (e.g., connection.close())
        # pass # Placeholder doesn't need closing

# --- RQ Task Function ---
def process_product_message(product_json_string):
    """
    This function is executed by the RQ worker for each job.
    It parses the JSON and calls the database insertion function.
    """
    logger.info(f"Processing job...")
    logger.debug(f"Received raw data: {product_json_string}")

    try:
        product_data = json.loads(product_json_string)
        logger.info(f"Parsed product data for ID: {product_data.get('id', 'N/A')}")

        # Get a database connection for this task
        db_conn = get_db_connection()

        if db_conn:
            success = insert_product_to_db(product_data, db_conn)
            # Close connection if necessary (depends on get_db_connection implementation)
            # if hasattr(db_conn, 'close'): db_conn.close() # Example
            logger.debug("Placeholder: 'Closed' database connection.")
        else:
            logger.error("Skipping database insertion due to connection failure.")
            # Force the job to fail if DB connection is essential
            raise ConnectionError("Failed to get database connection.")

        if success:
            logger.info(f"Successfully processed product ID: {product_data.get('id', 'N/A')}")
            # RQ considers the job successful if no exception is raised
        else:
            logger.error(f"Failed to process product ID: {product_data.get('id', 'N/A')}")
            # Raise an exception to mark the job as failed in RQ
            raise RuntimeError(f"Database insertion failed for product ID: {product_data.get('id', 'N/A')}")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}", exc_info=True)
        logger.error(f"Problematic data snippet: {product_json_string[:200]}")
        # Let RQ handle the failure by raising the exception
        raise ValueError(f"Invalid JSON format: {e}") from e
    except Exception as e:
        logger.error(f"An unexpected error occurred processing job: {e}", exc_info=True)
        # Re-raise the exception so RQ marks the job as failed
        raise

# --- Main Worker Execution ---
if __name__ == "__main__":
    logger.info("Starting RQ Consumer...")
    # ... (Redis connection setup remains the same) ...
    try:
        redis_connection = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )
        redis_connection.ping()
        logger.info("Redis connection successful.")
    except redis_exceptions.ConnectionError as e:
        logger.error(f"Could not connect to Redis: {e}", exc_info=True)
        exit(1)
    except Exception as e:
         logger.error(f"An unexpected error occurred during Redis connection: {e}", exc_info=True)
         exit(1)

    # ---- CHANGES START HERE ----

    # Remove the 'with Connection(redis_connection):' block

    # Pass the connection directly to Queue and Worker
    queues = [Queue(RQ_QUEUE_NAME, connection=redis_connection)]
    worker = Worker(queues, connection=redis_connection) # Pass connection here too

    # ---- CHANGES END HERE ----

    logger.info("Worker starting... Press Ctrl+C to exit.")
    try:
        worker.work(with_scheduler=False)
    except KeyboardInterrupt:
         logger.info("Worker shutting down...")
    except Exception as e:
         logger.error(f"Worker encountered critical error: {e}", exc_info=True)
    finally:
         logger.info("Worker stopped.")