import asyncio
import logging
import os
import signal
import socket
from consumer import run_worker
from consumer import redis_conn
from models import engine as db_engine
from dotenv import load_dotenv


load_dotenv()


NUM_WORKERS = int(os.getenv('NUM_CONSUMER_WORKERS', '3'))
WORKER_NAME_PREFIX = os.getenv('CONSUMER_NAME_PREFIX', 'consumer')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('MainApp')


running_tasks = []
shutdown_event = asyncio.Event()


def handle_shutdown_signal(sig, frame):
    logger = logging.getLogger('SignalHandler')

    if not shutdown_event.is_set():
        logger.warning(f'Received signal {sig}. Initiating graceful shutdown...')
        shutdown_event.set()

    else:
        logger.warning(f'Received signal {sig} again. Shutdown already in progress.')


async def main():
    logger.info('Application starting...')

    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handle_shutdown_signal, sig, None)

    logger.info(f'Starting {NUM_WORKERS} consumer workers...')
    hostname = socket.gethostname()

    for i in range(NUM_WORKERS):
        consumer_name = f'{WORKER_NAME_PREFIX}-{hostname}-{i+1}'

        task = asyncio.create_task(run_worker(consumer_name, shutdown_event), name=f'Worker-{consumer_name}')
        running_tasks.append(task)

    logger.info('All workers started. Waiting for shutdown signal (Ctrl+C)...')

    await shutdown_event.wait()

    logger.info('Shutdown signal received. Waiting for worker tasks to complete...')

    timeout_seconds = 30.0

    try:
        done, pending = await asyncio.wait(running_tasks, timeout=timeout_seconds)

        if pending:
            logger.warning(f'{len(pending)} worker tasks did not finish within {timeout_seconds}s timeout. Attempting to cancel...')

            for task in pending:
                task.cancel()

            await asyncio.gather(*pending, return_exceptions=True)
            logger.info('Cancellation attempts finished.')

        else:
             logger.info('All worker tasks completed gracefully.')

    except Exception as e:
        logger.exception('An error occurred while waiting for worker tasks.')


    logger.info('Starting resource cleanup...')

    try:
        if redis_conn:
            await redis_conn.aclose()
            logger.info('Closed Redis connection.')
        
        else:
            logger.info('Redis connection already closed or not initialized.')

    except Exception as e:
        logger.error(f'Error closing Redis connection: {e}')

    try:
        if db_engine:
            await db_engine.dispose()
            logger.info('Disposed of database engine connections.')
        
        else:
             logger.warning('Database engine not initialized.')
    
    except Exception as e:
        logger.error(f'Error disposing database engine: {e}')

    logger.info('Application shutdown complete.')


if __name__ == '__main__':
    asyncio.run(main())