import os
import logging
from typing import Any, Dict, Optional, List
from decimal import Decimal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
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


logger = logging.getLogger(__name__)


def get_db_connection() -> Optional[Session]:
    """
    Create and return a new SQLModel Session for database operations.
    """
    try:
        session = Session(engine)
        logger.info("Database session created successfully.")
        return session
    except Exception as e:
        logger.error(f"Failed to create database session: {e}", exc_info=True)
        return None


def insert_product_to_db(product_data: Dict[str, Any], session: Session) -> bool:
    """
    Insert or update a Product record based on incoming JSON data.

    Expects product_data to have keys matching the Product model fields,
    e.g., supermarket_id, name, sku, price, created_at.
    """
    try:
        # Instantiate Product model from JSON payload
        product = Product(**product_data)

        # Add to session and commit (upsert behaviour via primary key)
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
        # Close the session to free resources
        session.close()
