import asyncio
import json
import logging
import os
import redis.asyncio as redis
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
import argparse

from models import Product, CategoryURLHTML, CategoryURL, ProductURLHTML, ProductURL, ProductHTML


load_dotenv()


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
DEFAULT_ITEM_COUNT = int(os.getenv("PRODUCER_ITEM_COUNT", "500"))
SLEEP_INTERVAL = float(os.getenv("PRODUCER_SLEEP", "0.01"))

MODEL_MAP = {
    'Product': Product,
    'CategoryURLHTML': CategoryURLHTML,
    'CategoryURL': CategoryURL,
    'ProductURLHTML': ProductURLHTML,
    'ProductURL': ProductURL,
    'ProductHTML': ProductHTML,
}

CATEGORY_URL_STREAM_NAME = os.getenv("CATEGORY_URL_STREAM_NAME", "category_url_stream")
CATEGORY_URL_HTML_STREAM_NAME = os.getenv("CATEGORY_URL_HTML_STREAM_NAME", "category_url_html_stream")

PRODUCT_URL_STREAM_NAME = os.getenv("PRODUCT_URL_STREAM_NAME", "product_url_stream")
PRODUCT_URL_HTML_STREAM_NAME = os.getenv("PRODUCT_URL_HTML_STREAM_NAME", "product_url_html_stream")

PRODUCT_STREAM_NAME = os.getenv("PRODUCT_STREAM_NAME", "products_stream")
PRODUCT_HTML_STREAM_NAME = os.getenv("PRODUCT_HTML_STREAM_NAME", "product_html_stream")

STREAM_MAP = {
    'Product': PRODUCT_STREAM_NAME,
    'CategoryURLHTML': CATEGORY_URL_HTML_STREAM_NAME,
    'CategoryURL': CATEGORY_URL_STREAM_NAME,
    'ProductURLHTML': PRODUCT_URL_HTML_STREAM_NAME,
    'ProductURL': PRODUCT_URL_STREAM_NAME,
    'ProductHTML': PRODUCT_HTML_STREAM_NAME,
}


async def push_items(n=DEFAULT_ITEM_COUNT, mode='stream', model_name='Product'):
    model_class = MODEL_MAP.get(model_name)
    target_stream_name = STREAM_MAP.get(model_name)

    if not model_class or not target_stream_name:
        logger.error(f"Unknown model name or stream mapping: {model_name}. Available models: {list(MODEL_MAP.keys())}")
        return

    logger.info(f"Starting producer in '{mode}' mode to push {n} items of model '{model_name}' to stream '{target_stream_name}'...")
    pushed_count = 0

    redis_conn = None

    try:
        redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

        await redis_conn.ping()

        logger.info("Connected to Redis.")

        def create_item_data(i, model_class):
            now_iso = datetime.now().isoformat()

            if model_class == Product:
                return Product(
                    supermarket_id=1,
                    description=f"Test Product {i+1}",
                    sku=f"SKU_{i+1:05d}",
                    price=Decimal((i + 1) * 1.25),
                    url=f"http://example.com/product/{i+1}",
                    created_at=now_iso
                )

            elif model_class == CategoryURLHTML:
                return CategoryURLHTML(
                    supermarket_id=1,
                    url=f"http://example.com/category-html/{i+1}",
                    html=f"<p>HTML content for category {i+1}</p>",
                    created_at=now_iso
                )

            elif model_class == CategoryURL:
                return CategoryURL(
                    supermarket_id=1,
                    description=f"Category {i+1}",
                    url=f"http://example.com/category/{i+1}",
                    created_at=now_iso
                )

            elif model_class == ProductURLHTML:
                return ProductURLHTML(
                    supermarket_id=1,
                    url=f"http://example.com/product-html-detail/{i+1}",
                    html=f"<div>Detailed HTML for product {i+1}</div>",
                    created_at=now_iso
                )

            elif model_class == ProductURL:
                return ProductURL(
                    supermarket_id=1,
                    description=f"Product URL {i+1}",
                    url=f"http://example.com/product-url/{i+1}",
                    created_at=now_iso
                )

            elif model_class == ProductHTML:
                return ProductHTML(
                    supermarket_id=1,
                    url=f"http://example.com/raw-product-html/{i+1}",
                    html=f"<body>Raw Product HTML {i+1}</body>",
                    created_at=now_iso
                )

            else:
                logger.error(f"Data creation not implemented for model: {model_class.__name__}")
                return None


        if mode == 'stream':
            for i in range(n):
                item = create_item_data(i, model_class)

                if item is None:
                    continue

                item_data = item.to_dict() if hasattr(item, 'to_dict') else item.__dict__

                message_payload = {"data": json.dumps(item_data, default=str)}

                message_id = await redis_conn.xadd(target_stream_name, message_payload)
                logger.debug(f"Streamed item {i+1} ({model_name}) to {target_stream_name}, message ID: {message_id}")

                pushed_count += 1

                await asyncio.sleep(SLEEP_INTERVAL)

        elif mode == 'bulk':
            logger.info(f"Generating {n} items for bulk push...")
            items_data = []

            for i in range(n):
                item = create_item_data(i, model_class)

                if item is None:
                    continue

                items_data.append(item)

            logger.info(f"Preparing pipeline for {len(items_data)} XADD commands to {target_stream_name}...")
            pipe = redis_conn.pipeline()

            for i, item in enumerate(items_data):
                item_data = item.to_dict() if hasattr(item, 'to_dict') else item.__dict__

                message_payload = {"data": json.dumps(item_data, default=str)}

                pipe.xadd(target_stream_name, message_payload)

                if (i + 1) % 100 == 0 or (i + 1) == len(items_data):
                    logger.debug(f"Queued XADD for item {i+1} ({model_name})")

            logger.info(f"Executing pipeline to push {len(items_data)} messages to {target_stream_name}...")

            message_ids = await pipe.execute()
            pushed_count = len(message_ids)

            logger.debug(f"Pipeline executed. Received {pushed_count} message IDs.")

        else:
            logger.error(f"Unknown mode: {mode}. Use 'stream' or 'bulk'.")
            return

    except Exception as e:
        logger.exception("An unexpected error occurred during production.")

    finally:
        logger.info(f"Producer finished. Pushed {pushed_count} items of model '{model_name}' to stream '{target_stream_name}' in '{mode}' mode.")

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
        default=DEFAULT_ITEM_COUNT,
        help=f"Number of items to push. Defaults to {DEFAULT_ITEM_COUNT} (or PRODUCER_ITEM_COUNT env var)."
    )

    parser.add_argument(
        "--sleep",
        type=float,
        default=SLEEP_INTERVAL,
        help=f"Sleep interval between messages in 'stream' mode (seconds). Defaults to {SLEEP_INTERVAL} (or PRODUCER_SLEEP env var)."
    )

    parser.add_argument(
        "--model",
        type=str,
        choices=list(MODEL_MAP.keys()),
        default='Product',
        help=f"The model type to push. Items will be sent to the corresponding stream ({STREAM_MAP}). Available models: {list(MODEL_MAP.keys())}. Defaults to 'Product'."
    )


    args = parser.parse_args()

    asyncio.run(push_items(n=args.count, mode=args.mode, model_name=args.model))