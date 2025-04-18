import asyncio
import json
import logging
import os
import redis.asyncio as redis
from redis.exceptions import ResponseError
from models import Product, AsyncSessionLocal
from dotenv import load_dotenv


load_dotenv()


STREAM_NAME = os.getenv("REDIS_STREAM_NAME", "products_stream")
GROUP_NAME = os.getenv("REDIS_GROUP_NAME", "product_db_inserters")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BATCH_SIZE = int(os.getenv("CONSUMER_BATCH_SIZE", "100"))
BLOCK_MS = int(os.getenv("CONSUMER_BLOCK_MS", "5000"))


redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


async def setup_consumer_group(logger):
    try:
        await redis_conn.xgroup_create(STREAM_NAME, GROUP_NAME, id='0', mkstream=True)
        logger.info(f"Created consumer group '{GROUP_NAME}' for stream '{STREAM_NAME}'.")
    
    except ResponseError as e:
        if "BUSYGROUP" in str(e):
            logger.info(f"Consumer group '{GROUP_NAME}' already exists.")
        
        else:
            logger.error(f"Failed to create/verify consumer group: {e}")
            raise


async def process_messages(consumer_name: str, messages: list, logger):
    if not messages:
        logger.debug("process_messages called with no messages.")
        return 0

    ids_to_ack_malformed = []
    models_to_insert = []
    ids_successfully_parsed = []

    for stream, entries in messages:
        if stream != STREAM_NAME:
             logger.warning(f"Received message from unexpected stream '{stream}'. Skipping.")
             continue

        for entry_id, fields in entries:
            logger.info(f"Worker {consumer_name} processing message {entry_id}: {fields}")

            if 'data' not in fields:
                logger.warning(f"Skipping entry {entry_id}: 'data' field missing.")
                ids_to_ack_malformed.append(entry_id)
                continue

            try:
                product_data = json.loads(fields["data"])
                product_model = Product(**product_data)

                models_to_insert.append(product_model)
                ids_successfully_parsed.append(entry_id)

            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Skipping entry {entry_id} due to parsing/validation error: {e}. Acknowledging message.")
                ids_to_ack_malformed.append(entry_id)

    successfully_inserted_count = 0
    ids_to_ack_db_success = []

    if models_to_insert:
        logger.info(f"Attempting to insert batch of {len(models_to_insert)} products into DB...")
        try:
            async with AsyncSessionLocal() as session:
                session.add_all(models_to_insert)
                await session.commit()

            logger.info(f"Successfully inserted batch of {len(models_to_insert)} products.")
            successfully_inserted_count = len(models_to_insert)
            ids_to_ack_db_success = ids_successfully_parsed

        except Exception as e:
            logger.exception(f"Database error inserting batch of {len(models_to_insert)} products. None of these messages will be acknowledged based on DB success.")

    final_ids_to_ack = ids_to_ack_malformed + ids_to_ack_db_success

    if final_ids_to_ack:
        try:
            logger.debug(f"Attempting to acknowledge messages: {final_ids_to_ack}")
            acked_count = await redis_conn.xack(STREAM_NAME, GROUP_NAME, *final_ids_to_ack)

            if acked_count == len(final_ids_to_ack):
                 logger.info(f"Acknowledged {acked_count} messages.")

            else:
                 logger.warning(f"Attempted to ACK {len(final_ids_to_ack)} messages, but Redis reported {acked_count} ACKs.")

        except Exception as e:
            logger.exception(f"Failed to acknowledge messages: {final_ids_to_ack}. These might be reprocessed.")

    return successfully_inserted_count


async def run_worker(consumer_name: str, shutdown_event: asyncio.Event):
    logger = logging.getLogger(f"Worker-{consumer_name}")
    logger.info(f"Starting...")
    
    await setup_consumer_group(logger)

    try:
        logger.debug(f"Worker {consumer_name} entering main loop. Shutdown requested: {shutdown_event.is_set()}")
        
        while not shutdown_event.is_set():
            logger.debug(f"Worker {consumer_name} top of loop. Shutdown requested: {shutdown_event.is_set()}")
            
            try:
                logger.debug(f"Worker {consumer_name} calling xreadgroup...")

                response = await redis_conn.xreadgroup(
                    GROUP_NAME, consumer_name, {STREAM_NAME: '>'},
                    count=BATCH_SIZE, block=BLOCK_MS,
                )

                logger.debug(f"Worker {consumer_name} xreadgroup returned. Response length: {len(response) if response else 0}. Shutdown requested: {shutdown_event.is_set()}")

                if shutdown_event.is_set():
                    logger.debug(f"Worker {consumer_name} Shutdown requested after xreadgroup returned. Breaking loop.")
                    break

                if response:
                     num_messages_in_batch = sum(len(entries) for _, entries in response)
                     logger.debug(f"Worker {consumer_name} processing {num_messages_in_batch} messages...")

                     successfully_inserted = await process_messages(consumer_name, response, logger)
                     logger.debug(f"Worker {consumer_name} finished processing batch. Successfully inserted {successfully_inserted}. Shutdown requested: {shutdown_event.is_set()}")

                else:
                     logger.debug(f"Worker {consumer_name} XREADGROUP timed out with no messages. Shutdown requested: {shutdown_event.is_set()}")

            except redis.exceptions.TimeoutError:
                 logger.debug(f"Worker {consumer_name} XREADGROUP timed out. Shutdown requested: {shutdown_event.is_set()}")
                 continue
            
            except redis.exceptions.ConnectionError as e:
                 logger.error(f"Worker {consumer_name} Redis connection error: {e}. Sleeping before retry...")
                 await asyncio.sleep(5)
            
                 if shutdown_event.is_set():
                      logger.debug(f"Worker {consumer_name} Shutdown requested after Redis connection error sleep. Breaking loop.")
                      break
            
            except Exception as e:
                logger.exception(f"Worker {consumer_name} An error occurred in the main worker loop.")
                await asyncio.sleep(2)
                
                if shutdown_event.is_set():
                     logger.debug(f"Worker {consumer_name} Shutdown requested after general error sleep. Breaking loop.")
                     break

    finally:
        logger.warning(f"Worker {consumer_name} exiting.")