import uvicorn
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func, desc, over
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from models import Supermarket, CategoryURL, ProductURL, Product, get_session


app = FastAPI(
    title="supermarket-py-backend",
    description="API for comparing prices of products across different supermarkets",
    version="1.0.0",
)


@app.get("/products")
async def get_all_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/search/")
async def search_products(query: str, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product).where(
            (Product.name.ilike(f"%{query}%"))
        ).order_by(Product.created_at.desc())
    ).all()
    
    return products


@app.post("/price-comparison")
async def price_comparison(shopping_list: List[dict], session: Session = Depends(get_session)):
    shopping_list = [{'sku': 'BREAD-WHT-500G', 'quantity': 1}]
    sku = 'BREAD-WHT-500G'
    
    # ROW_NUMBER() OVER(PARTITION BY product.supermarket_id, ORDER BY product.created_at DESC)
    row_number_expr = func.row_number().over(
        partition_by=Product.supermarket_id,
        order_by=desc(Product.created_at)
    )

    subquery = (
        select(
            Product.id,
            Product.supermarket_id,
            Product.name,
            Product.sku,
            Product.price,
            Product.created_at,
            row_number_expr.label("row_n")
        )
        .where(Product.sku == sku)
        .subquery()
    )

    stmt = (
        select(subquery.c.supermarket_id,
               subquery.c.name,
               subquery.c.sku,
               subquery.c.price,
               subquery.c.created_at)
        .where(subquery.c.row_n == 1)
    )

    results = session.exec(stmt).all()
    print(pd.DataFrame(results).sort_values(by='price', ascending=True))
    
    return {"status": "/products/price-comparison"}


@app.post("/inflation")
async def calculate_inflation(shopping_list: dict, date_range: List[str], session: Session = Depends(get_session)):
    shopping_list = [{'sku': 'BREAD-WHT-500G', 'quantity': 1}]
    start_date, end_date = ['2025-01-01', '2025-02-01']
    # calculate average inflation
    # calculate lowest inflation
    # calculate gap inflation
    
    return {"status": "/inflation"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)