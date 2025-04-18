import os
import logging
from typing import Any, Dict, Optional, List
from decimal import Decimal
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlmodel import Field, SQLModel, Relationship
from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger(__name__)


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'supermarket')
IS_PROD = os.getenv('IS_PROD', 'False') == 'True'

if IS_PROD:
    DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?ssl=require'
    logger.info("Using Production Database URL with SSL.")

else:
    DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    logger.info("Using Development Database URL.")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Supermarket(SQLModel, table=True):
    __tablename__ = 'supermarkets'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    home_url: Optional[str] = None
    category_urls_container_url: Optional[str] = None
    category_urls_container_class: Optional[str] = None
    api_url: Optional[str] = None
    
    category_urls: List['CategoryURL'] = Relationship(back_populates='supermarket')
    product_urls: List['ProductURL'] = Relationship(back_populates='supermarket')
    products: List['Product'] = Relationship(back_populates='supermarket')


class CategoryURL(SQLModel, table=True):
    __tablename__ = 'category_urls'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key='supermarkets.id')
    description: str
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    supermarket: Supermarket = Relationship(back_populates='category_urls')


class ProductURL(SQLModel, table=True):
    __tablename__ = 'product_urls'

    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key='supermarkets.id')
    description: str
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    supermarket: Supermarket = Relationship(back_populates='product_urls')


class Product(SQLModel, table=True):
    __tablename__ = 'products'

    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key='supermarkets.id')
    description: str
    sku: str
    price: Decimal
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    supermarket: Optional[Supermarket] = Relationship(back_populates='products')