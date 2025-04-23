import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Type

import redis.asyncio as redis
from redis.exceptions import ResponseError

from models import Product, CategoryURLHTML, CategoryURL, ProductURLHTML, ProductURL, ProductHTML, ProductURL, AsyncSessionLocal
from dotenv import load_dotenv

load_dotenv()


CATEGORY_URL_STREAM_NAME = os.getenv("CATEGORY_URL_STREAM_NAME", "category_urls_stream")
CATEGORY_URL_HTML_STREAM_NAME = os.getenv("CATEGORY_URL_HTML_STREAM_NAME", "category_urls_html_stream")

PRODUCT_URL_STREAM_NAME = os.getenv("PRODUCT_URL_STREAM_NAME", "product_urls_stream")
PRODUCT_URL_HTML_STREAM_NAME = os.getenv("PRODUCT_URL_HTML_STREAM_NAME", "product_urls_html_stream")

PRODUCT_STREAM_NAME = os.getenv("PRODUCT_STREAM_NAME", "products_stream")
PRODUCT_HTML_STREAM_NAME = os.getenv("PRODUCT_HTML_STREAM_NAME", "products_html_stream")


STREAM_MODEL_MAP: Dict[str, Type] = {
    CATEGORY_URL_HTML_STREAM_NAME: CategoryURLHTML,
    CATEGORY_URL_STREAM_NAME: CategoryURL,
    PRODUCT_URL_HTML_STREAM_NAME: ProductURLHTML,
    PRODUCT_URL_STREAM_NAME: ProductURL,
    PRODUCT_HTML_STREAM_NAME: ProductHTML,
    PRODUCT_STREAM_NAME: Product
}


GROUP_NAME = os.getenv("REDIS_GROUP_NAME", "product_db_inserters")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BATCH_SIZE = int(os.getenv("CONSUMER_BATCH_SIZE", "100"))
BLOCK_MS = int(os.getenv("CONSUMER_BLOCK_MS", "5000"))
MAX_STREAM_LENGTH = int(os.getenv("MAX_STREAM_LENGTH", 10_000))

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def setup_consumer_groups(logger: logging.Logger) -> None:
    for stream in STREAM_MODEL_MAP.keys():
        try:
            await redis_conn.xgroup_create(stream, GROUP_NAME, id="0", mkstream=True)
            logger.info(f"Created consumer group '{GROUP_NAME}' for stream '{stream}'.")

        except ResponseError as e:
            if "BUSYGROUP" in str(e):
                logger.info(f"Consumer group '{GROUP_NAME}' already exists on '{stream}'.")

            else:
                logger.error(f"Could not create consumer group on '{stream}': {e}")
                raise


async def process_messages(consumer_name: str, messages: List, logger: logging.Logger) -> int:
    if not messages:
        return 0

    bucket: Dict[Type, List] = {model: [] for model in STREAM_MODEL_MAP.values()}
    ack_success: List[str] = []
    ack_malformed: List[str] = []

    for stream, entries in messages:
        model_cls = STREAM_MODEL_MAP.get(stream)
        
        if model_cls is None:
            logger.warning(f"Unknown stream '{stream}' – skipping.")
            continue

        for entry_id, fields in entries:
            raw = fields.get("data")
        
            if raw is None:
                logger.warning(f"{entry_id}: missing 'data' field – skipping/ACKing.")
                ack_malformed.append(entry_id)
                continue

            try:
                data = json.loads(raw)
                data['created_at'] = datetime.fromisoformat(data['created_at'])
                
                bucket[model_cls].append(model_cls(**data))
                ack_success.append(entry_id)
            
            except Exception as e:
                logger.warning(f"{entry_id}: parse/validation error: {e} – skipping.")
                ack_malformed.append(entry_id)

    total_inserted = sum(len(entries) for entries in bucket.values())

    if total_inserted:
        logger.info(f"Inserting batch of {total_inserted} objects into DB...")

        try:
            async with AsyncSessionLocal() as session:
                for obj in bucket.values():
                    session.add_all(obj)

                await session.commit()

            logger.info("DB commit successful.")

        except Exception:
            logger.exception("DB commit failed – nothing has been ACKed.")
            ack_success.clear()
            total_inserted = 0

    ids_to_ack = ack_malformed + ack_success
    
    if ids_to_ack:
        try:
            await redis_conn.xack(*([stream for stream in STREAM_MODEL_MAP.keys()][0:1]), GROUP_NAME, *ids_to_ack)
        
        except Exception:
            logger.exception(f"Failed to ACK {len(ids_to_ack)} messages.")

    try:
        for stream in STREAM_MODEL_MAP.keys():
            trimmed = await redis_conn.xtrim(stream, maxlen=MAX_STREAM_LENGTH, approximate=False)
            
            if trimmed:
                logger.debug(f"XTRIM {stream}: removed {trimmed} old entries.")
    
    except Exception:
        logger.exception("Failed to XTRIM stream(s).")

    return total_inserted


async def run_worker(consumer_name: str, shutdown_event: asyncio.Event):
    logger = logging.getLogger(f"Worker-{consumer_name}")
    logger.info("Starting…")

    await setup_consumer_groups(logger)

    streams_dict = {s: ">" for s in STREAM_MODEL_MAP.keys()}

    try:
        while not shutdown_event.is_set():
            try:
                response = await redis_conn.xreadgroup(
                    GROUP_NAME,
                    consumer_name,
                    streams_dict,
                    count=BATCH_SIZE,
                    block=BLOCK_MS,
                )
                
                if response:
                    await process_messages(consumer_name, response, logger)

            except redis.exceptions.TimeoutError:
                pass
            
            except redis.exceptions.ConnectionError as e:
                logger.error(f"Redis connection error: {e}. Retrying in 5 s…")
                await asyncio.sleep(5)
            
            except Exception:
                logger.exception("Unhandled error in worker loop; continuing.")
                await asyncio.sleep(2)

    finally:
        logger.warning("Exiting worker.")