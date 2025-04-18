import asyncio
import json
import logging
import os
import redis.asyncio as redis
from dotenv import load_dotenv
import argparse


load_dotenv()


STREAM_NAME = os.getenv("REDIS_STREAM_NAME", "products_stream")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
PRODUCT_COUNT = int(os.getenv("PRODUCER_PRODUCT_COUNT", "500"))
SLEEP_INTERVAL = float(os.getenv("PRODUCER_SLEEP", "0.01"))


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


async def push_products(n=PRODUCT_COUNT, mode='stream'):
	logger.info(f"Starting producer in '{mode}' mode to push {n} products to stream '{STREAM_NAME}'...")
	pushed_count = 0
	
	redis_conn = None
	
	try:
		redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
		
		await redis_conn.ping()
		
		logger.info("Connected to Redis.")

		if mode == 'stream':
			for i in range(n):
				product = {
					"supermarket_id": 1,
					"description": f"Test Product {i+1}",
					"sku": f"SKU_{i+1:05d}",
					"price": float((i + 1) * 1.25),
					"url": f"http://example.com/product/{i+1}"
				}

				message_id = await redis_conn.xadd(STREAM_NAME, {"data": json.dumps(product)})
				logger.debug(f"Streamed product {i+1}, message ID: {message_id}")

				pushed_count += 1
				
				await asyncio.sleep(SLEEP_INTERVAL)

		elif mode == 'bulk':
			logger.info(f"Generating {n} products for bulk push...")
			products_data = []
			
			for i in range(n):
				product = {
					"supermarket_id": 1,
					"description": f"Test Product {i+1}",
					"sku": f"SKU_{i+1:05d}",
					"price": float((i + 1) * 1.25),
					"url": f"http://example.com/product/{i+1}"
				}
				
				products_data.append(product)

			logger.info(f"Preparing pipeline for {n} XADD commands...")
			pipe = redis_conn.pipeline()
			
			for i, product in enumerate(products_data):
				pipe.xadd(STREAM_NAME, {"data": json.dumps(product)})

				if (i + 1) % 100 == 0 or (i + 1) == n:
					logger.debug(f"Queued XADD for product {i+1}")


			logger.info(f"Executing pipeline to push {n} messages...")

			message_ids = await pipe.execute()
			pushed_count = len(message_ids)

			logger.debug(f"Pipeline executed. Received {pushed_count} message IDs.")

		else:
			logger.error(f"Unknown mode: {mode}. Use 'stream' or 'bulk'.")
			return

	except redis.exceptions.ConnectionError as e:
		logger.error(f"Redis connection error: {e}")
	
	except Exception as e:
		logger.exception("An unexpected error occurred during production.")
	
	finally:
		logger.info(f"Producer finished. Pushed {pushed_count} products in '{mode}' mode.")

		if redis_conn:
			 await redis_conn.aclose()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Redis Stream Producer")
	
	parser.add_argument(
		"--mode",
		type=str,
		choices=['stream', 'bulk'],
		default='stream',
		help="Producer mode: 'stream' (one by one) or 'bulk' (pipeline). Defaults to 'stream'."
	)
	
	parser.add_argument(
		"--count",
		type=int,
		default=PRODUCT_COUNT,
		help=f"Number of products to push. Defaults to {PRODUCT_COUNT} (or PRODUCER_PRODUCT_COUNT env var)."
	)

	parser.add_argument(
		"--sleep",
		type=float,
		default=SLEEP_INTERVAL,
		help=f"Sleep interval between messages in 'stream' mode (seconds). Defaults to {SLEEP_INTERVAL} (or PRODUCER_SLEEP env var)."
	)
	
	args = parser.parse_args()

	PRODUCT_COUNT = args.count
	SLEEP_INTERVAL = args.sleep

	asyncio.run(push_products(n=PRODUCT_COUNT, mode=args.mode))
