import os
import logging
from typing import Any, Dict, Optional, List
from decimal import Decimal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger(__name__)


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'supermarket')


if os.getenv('IS_PROD') == 'True':
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}?sslmode=require'
    # DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}?sslmode=require'

else:
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


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

    supermarket: Supermarket = Relationship(back_populates='products')


engine = create_engine(DATABASE_URL)

# engine = create_async_engine(DATABASE_URL, echo=True, pool_size=20, max_overflow=80, future=True)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         yield session

def get_db_connection() -> Optional[Session]:
    try:
        session = Session(engine)
        logger.info("Database session created successfully.")
    
        return session
    
    except Exception as e:
        logger.error(f"Failed to create database session: {e}", exc_info=True)
    
        return None


def insert_product_to_db(product_data: Dict[str, Any], session: Session) -> bool:
    try:
        product = Product(**product_data)

        session.add(product)
        session.commit()
        session.refresh(product)
    
        logger.info(f"Inserted/updated product ID: {product.description}")
    
        return True
    
    except Exception as e:
        logger.error(f"Failed to insert/update product: {e}", exc_info=True)
        session.rollback()
    
        return False
    
    finally:
        session.close()

# async def insert_product_to_db(product_data: Dict[str, Any], session: AsyncSession) -> bool:
#     try:
#         product = Product(**product_data)
        
#         session.add(product)
#         await session.commit()
#         await session.refresh(product)
        
#         logger.info(f"Inserted/updated product ID: {product.id}")
        
#         return True

#     except Exception as e:
#         logger.error(f"Failed to insert/update product: {e}", exc_info=True)
#         await session.rollback()
        
#         return False