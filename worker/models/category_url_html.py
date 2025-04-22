from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

from models.supermarket import Supermarket


class CategoryURLHTML(SQLModel, table=True):
    __tablename__ = 'category_urls_html'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    supermarket_id: int = Field(foreign_key='supermarkets.id')
    html: str
    url: str
    created_at: datetime = Field(default_factory=datetime.now)