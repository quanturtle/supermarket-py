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
    all_results = []
    
    for prod in shopping_list:
        # ROW_NUMBER() OVER(PARTITION BY product.supermarket_id, ORDER BY product.created_at DESC)
        row_number_expr = func.row_number().over(
            partition_by=Product.supermarket_id,
            order_by=desc(Product.created_at)
        )

        # SELECT *, ROW_NUMBER() OVER(...) FROM products
        subquery = (
            select(
                Product.id,
                Product.supermarket_id,
                Product.name,
                Product.sku,
                Product.price,
                Product.created_at,
                row_number_expr.label('row_n')
            )
            .where(Product.sku == prod['sku'])
            .subquery()
        )

        # SELECT * FROM subquery WHERE row_num == 1
        stmt = (
            select(
                subquery.c.supermarket_id,
                subquery.c.name,
                subquery.c.sku,
                subquery.c.price,
                subquery.c.created_at)
            .where(subquery.c.row_n == 1)
        )

        results = session.exec(stmt).all()
        all_results += results
        
    price_df = pd.DataFrame(all_results).sort_values(by='price', ascending=True)

    # for each product, lowest prices regardless of supermarket
    optimal_df = price_df.loc[price_df.groupby('sku')['price'].idxmin()]

    # group by supermarket and get the shopping list price
    price_totals_df = price_df.groupby('supermarket_id')['price'].sum().sort_values(ascending=True)

    # best
    best_supermarket_id = price_totals_df.idxmin()
    best_supermarket_df = price_df[price_df["supermarket_id"] == best_supermarket_id]

    # median
    median_idx = len(price_totals_df) // 2
    median_supermarket_id = price_totals_df.index[median_idx]
    median_supermarket_df = price_df[price_df["supermarket_id"] == median_supermarket_id]

    # worst
    worst_supermarket_id = price_totals_df.idxmax()
    worst_supermarket_df = price_df[price_df["supermarket_id"] == worst_supermarket_id]

    return {
        "optimal": optimal_df.to_dict(orient='records'),
        "best": best_supermarket_df.to_dict(orient='records'),
        "median": median_supermarket_df.to_dict(orient='records'),
        "worst": worst_supermarket_df.to_dict(orient='records')
    }


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