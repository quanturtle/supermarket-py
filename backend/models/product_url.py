from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

from models.supermarket import Supermarket


class ProductURL(SQLModel, table=True):
    __tablename__ = "product_urls"
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key="supermarkets.id")
    description: str
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    supermarket: Supermarket = Relationship(back_populates="product_urls")