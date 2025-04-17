# consumer.py
import asyncio
import json
import logging
import redis.asyncio as redis
from redis.exceptions import LockError
from sqlmodel import SQLModel
from models import Product, engine, get_session

STREAM_NAME = "products_stream"
OFFSET_KEY = "stream_offset"
LOCK_KEY = "stream_lock"
BATCH_SIZE = 100
LOCK_TIMEOUT = 60

redis_conn = redis.Redis(decode_responses=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


async def run_worker(worker_id: int):
    logger = logging.getLogger(f"Worker-{worker_id}")
    while True:
        try:
            lock = redis_conn.lock(LOCK_KEY, timeout=LOCK_TIMEOUT, blocking_timeout=5)
            got_lock = await lock.acquire()

            if not got_lock:
                await asyncio.sleep(1)
                continue

            last_id = await redis_conn.get(OFFSET_KEY)
            start_id = f"({last_id}" if last_id else "-"

            entries = await redis_conn.xrange(STREAM_NAME, min=start_id, max="+", count=BATCH_SIZE)

            if not entries:
                logger.info("No new stream entries.")
                await asyncio.sleep(1)
                continue

            batch = []
            for entry_id, fields in entries:
                try:
                    product_data = json.loads(fields["data"])
                    batch.append(Product(**product_data))
                except Exception as e:
                    logger.warning(f"Skipping entry {entry_id}: {e}")

            async with await get_session() as session:
                session.add_all(batch)
                await session.commit()
                logger.info(f"Inserted {len(batch)} products to DB.")

            last_entry_id = entries[-1][0]
            await redis_conn.set(OFFSET_KEY, last_entry_id)
            logger.info(f"Advanced offset to {last_entry_id}")

        except LockError:
            logger.warning("Failed to acquire lock.")
        except Exception as e:
            logger.exception("Worker error")
        finally:
            try:
                await lock.release()
            except Exception:
                pass
            await asyncio.sleep(0.5)