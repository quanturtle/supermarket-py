from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "price_comparison")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


class Supermarket(SQLModel, table=True):
    __tablename__ = "supermarkets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    home_url: Optional[str] = None
    categories_container_url: Optional[str] = None
    categories_container_class: Optional[str] = None
    api_url: Optional[str] = None
    
    category_urls: List["CategoryURL"] = Relationship(back_populates="supermarket")


class CategoryURL(SQLModel, table=True):
    __tablename__ = "category_urls"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key="supermarkets.id")
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    supermarket: Supermarket = Relationship(back_populates="category_urls")


class ProductURL(SQLModel, table=True):
    __tablename__ = "product_urls"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Product(SQLModel, table=True):
    __tablename__ = "products"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sku: str
    price: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


def get_session():
    with Session(engine) as session:
        yield session