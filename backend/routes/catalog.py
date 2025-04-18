from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from models import Product, Supermarket, get_session


router = APIRouter(prefix="", tags=["catalog"])
catalog_router = router


@router.get('/catalog')
async def get_catalog(session: Session = Depends(get_session)):
    query = select(Product.id, Product.description, Product.sku).distinct(Product.sku)
    return session.exec(query).mappings().all()