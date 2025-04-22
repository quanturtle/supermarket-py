from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


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