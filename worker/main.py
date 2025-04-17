# main.py
import asyncio
from consumer import run_worker

async def main():
    tasks = [asyncio.create_task(run_worker(i)) for i in range(1, 6)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
