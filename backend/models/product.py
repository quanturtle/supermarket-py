from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

from models.supermarket import Supermarket


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key="supermarkets.id")
    description: str
    sku: str
    price: Decimal
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    supermarket: Supermarket = Relationship(back_populates="products")