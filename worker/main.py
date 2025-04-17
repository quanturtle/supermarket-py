# main.py
import os
import logging
from dotenv import load_dotenv
from redis import Redis, exceptions as redis_exceptions
from rq import Queue, Worker

# Load environment variables at the start
load_dotenv()

# --- Configuration Variables ---
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD') or None
REDIS_DB = int(os.getenv('REDIS_DB', 0))
RQ_QUEUE_NAME = os.getenv('RQ_QUEUE_NAME', 'default')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# --- Configure Logging ---
log_level_int = getattr(logging, LOG_LEVEL, logging.INFO)
logging.basicConfig(
    level=log_level_int,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# Silence noisy libraries if needed (adjust level as preferred)
logging.getLogger("rq.worker").setLevel(logging.WARNING)
logging.getLogger("rq.job").setLevel(logging.INFO)

# --- Main Worker Execution ---
if __name__ == "__main__":
    logger.info("Starting RQ Worker Main...")
    logger.info(f"Listening on queue: '{RQ_QUEUE_NAME}'")

    # Establish Redis connection for the worker
    # IMPORTANT: No decode_responses=True for RQ worker connection
    try:
        redis_connection = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )
        redis_connection.ping()
        logger.info(f"Redis connection successful: {REDIS_HOST}:{REDIS_PORT} DB: {REDIS_DB}")

    except redis_exceptions.ConnectionError as e:
        logger.error(f"Could not connect to Redis: {e}", exc_info=True)
        exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred during Redis connection: {e}", exc_info=True)
        exit(1)

    # Define the queues the worker will listen to
    # Note: The worker needs access to the 'consumer.py' module to import the task function
    # This usually works fine if main.py and consumer.py are in the same directory
    # or if the project is structured as a package.
    queues_to_listen = [Queue(RQ_QUEUE_NAME, connection=redis_connection)]

    # Create the worker instance
    worker = Worker(queues_to_listen, connection=redis_connection)

    logger.info("Worker starting processing loop... Press Ctrl+C to exit.")
    try:
        # Start processing jobs. This call blocks.
        worker.work(with_scheduler=False) # Set burst=True to run once and exit
    except KeyboardInterrupt:
        logger.info("Worker shutting down...")
    except Exception as e:
        # Catch potential errors during worker setup or the work loop itself
        logger.error(f"Worker encountered critical error: {e}", exc_info=True)
    finally:
        # Cleanup can happen here if needed (e.g., closing a global DB pool)
        logger.info("Worker stopped.")