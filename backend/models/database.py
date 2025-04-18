import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv


load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'supermarket')


if os.getenv('IS_PROD') == 'True':
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}?sslmode=require'
else:
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session