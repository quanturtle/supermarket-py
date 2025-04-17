import asyncio
import json
import redis.asyncio as redis

STREAM_NAME = "products_stream"
redis_conn = redis.Redis(decode_responses=True)

async def push_products(n=500):
    for i in range(n):
        product = {
            "supermarket_id": 1,
            "description": f"Product {i+1}",
            "price": (i + 1) * 1.25,
            "url": f"hello.com/{i}"
        }

        await redis_conn.xadd(STREAM_NAME, {"data": json.dumps(product)})
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(push_products())
