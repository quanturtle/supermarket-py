import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from models import Supermarket, CategoryURL, ProductURL, Product, get_session


app = FastAPI(
    title="supermarket-py-backend",
    description="API for comparing prices of products across different supermarkets",
    version="1.0.0",
)


@app.get("/products")
async def get_all_products(db: Session = Depends(get_session)):
    return {"status": "/products"}


@app.get("/products/{product_id}")
async def get_product_by_id(db: Session = Depends(get_session)):
    return {"status": "/products/id"}


@app.get("/products/search/")
async def search_products(db: Session = Depends(get_session)):
    return {"status": "/products/search"}


@app.post("/price-comparison")
async def price_comparison(db: Session = Depends(get_session)):
    return {"status": "/products/price-comparison"}


@app.post("/inflation")
async def calculate_inflation(db: Session = Depends(get_session)):
    return {"status": "/inflation"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)