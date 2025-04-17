# consumer.py
import logging
import json
import models # Import the database functions module

# Setup logger for this module
logger = logging.getLogger(__name__)

# --- RQ Task Function ---
def process_product_message(product_json_string):
    """
    This function is executed by the RQ worker for each job.
    It parses the JSON and calls the database insertion function from models.py.
    """
    logger.info(f"Processing job...")
    logger.debug(f"Received raw data: {product_json_string}")

    try:
        product_data = json.loads(product_json_string)
        logger.info(f"Parsed product data for ID: {product_data.get('id', 'N/A')}")

        # Get a database connection for this task using the function from models
        db_conn = models.get_db_connection()

        success = False # Initialize success flag
        if db_conn:
            try:
                success = models.insert_product_to_db(product_data, db_conn)
                # Close connection if necessary (depends on get_db_connection implementation)
                # e.g., if get_db_connection returns a real connection object:
                # if hasattr(db_conn, 'close'):
                #     db_conn.close()
                #     logger.debug("Closed database connection.")
                # else:
                #     logger.debug("Placeholder: 'Closed' database connection.")
                logger.debug("Placeholder: 'Closed' database connection.")
            except Exception as db_exc:
                 logger.error(f"Error during database operation: {db_exc}", exc_info=True)
                 success = False
                 # Optionally re-raise or handle specific DB exceptions differently
                 # raise # Re-raise to mark job as failed immediately

        else:
            logger.error("Skipping database insertion due to connection failure.")
            # Force the job to fail if DB connection is essential
            # Setting success to False and raising error later ensures logging before failure
            success = False
            # raise ConnectionError("Failed to get database connection.") # Option to fail fast

        # Final status check after operations
        if success:
            logger.info(f"Successfully processed product ID: {product_data.get('id', 'N/A')}")
            # RQ considers the job successful if no exception is raised
        else:
            logger.error(f"Failed to process product ID: {product_data.get('id', 'N/A')}")
            # Raise an exception to mark the job as failed in RQ
            # Choose an appropriate error type
            raise RuntimeError(f"Processing failed for product ID: {product_data.get('id', 'N/A')}")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}", exc_info=True)
        logger.error(f"Problematic data snippet: {product_json_string[:200]}")
        # Let RQ handle the failure by raising the exception
        raise ValueError(f"Invalid JSON format: {e}") from e
    except Exception as e:
        # Catch any other unexpected errors during processing
        logger.error(f"An unexpected error occurred processing job: {e}", exc_info=True)
        # Re-raise the exception so RQ marks the job as failed
        raise