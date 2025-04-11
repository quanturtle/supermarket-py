from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
import os
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "supermarket")

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}?sslmode=require'
engine = create_engine(DATABASE_URL)


class Supermarket(SQLModel, table=True):
    __tablename__ = "supermarkets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    home_url: Optional[str] = None
    category_urls_container_url: Optional[str] = None
    category_urls_container_class: Optional[str] = None
    api_url: Optional[str] = None
    
    category_urls: List["CategoryURL"] = Relationship(back_populates="supermarket")
    products: List["Product"] = Relationship(back_populates="supermarket")


class CategoryURL(SQLModel, table=True):
    __tablename__ = "category_urls"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key="supermarkets.id")
    url: str
    created_at: datetime = Field(default_factory=datetime.now())
    
    supermarket: Supermarket = Relationship(back_populates="category_urls")


class ProductURL(SQLModel, table=True):
    __tablename__ = "product_urls"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.now())


class Product(SQLModel, table=True):
    __tablename__ = "products"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key="supermarkets.id")
    name: str
    sku: str
    price: Decimal
    created_at: datetime = Field(default_factory=datetime.now())

    supermarket: Supermarket = Relationship(back_populates="products")


def get_session():
    with Session(engine) as session:
        yield session