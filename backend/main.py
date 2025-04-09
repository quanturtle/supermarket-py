from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

import uvicorn
import pandas as pd
from sqlmodel import Session, select
from sqlalchemy import func, desc, over
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product, get_session


app = FastAPI(
    title='supermarket-py-backend',
    description='API for comparing prices of products across different supermarkets',
    version='1.0.0',
)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


@app.get('/products')
async def get_products(session: Session = Depends(get_session)):
    query = select(Product.id, Product.name, Product.sku).distinct(Product.sku)
    return session.exec(query).mappings().all()


@app.get('/products/{product_sku}')
async def get_product_by_sku(product_sku: str, session: Session = Depends(get_session)):
    seven_days_ago = datetime.today().date() - timedelta(days=7)

    price_history_stmt = (
        select(
            Product.supermarket_id,
            Product.name,
            Product.price,
            Product.created_at
        )
        .where(Product.sku == product_sku)
        .where(seven_days_ago <= Product.created_at)
    )
    
    price_history = session.exec(price_history_stmt).all()
    latest_product_prices_df = pd.DataFrame(price_history).sort_values(by=['supermarket_id', 'created_at'], ascending=[True, True])

    product_price_changes = []
    
    for supermarket_id, group in latest_product_prices_df.groupby('supermarket_id'):
        start_date_price = group[group['created_at'] == group['created_at'].min()]['price'].values[0]
        end_date_price = group[group['created_at'] == group['created_at'].max()]['price'].values[0]
        
        # Avoid division by zero
        if start_date_price > 0:  
            pct_change = ((end_date_price - start_date_price) / start_date_price) * 100
        else:
            pct_change = 0
            
        # Create record for this supermarket's price change
        price_change_record = {
            'supermarket_id': supermarket_id,
            'price': start_date_price,
            'pct_change': round(pct_change, 2)
        }
        
        product_price_changes.append(price_change_record)

    return {
        'history': latest_product_prices_df.to_dict(orient='records'),
        'product_info': {
            'name': latest_product_prices_df.iloc[0]['name'], 
            'sku': product_sku
        },
        'price_changes': product_price_changes
    }


@app.get('/products/search/')
async def search_products(query: str, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product).where(
            (Product.name.ilike(f'%{query}%'))
        ).order_by(Product.created_at.desc())
    ).all()
    
    return products


@app.post('/price-comparison')
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
    best_supermarket_df = price_df[price_df['supermarket_id'] == price_totals_df.idxmin()]

    # median
    median_supermarket_id = price_totals_df.index[len(price_totals_df) // 2]
    median_supermarket_df = price_df[price_df['supermarket_id'] == median_supermarket_id]

    # worst
    worst_supermarket_df = price_df[price_df['supermarket_id'] == price_totals_df.idxmax()]

    return {
        'optimal': optimal_df.to_dict(orient='records'),
        'best': best_supermarket_df.to_dict(orient='records'),
        'median': median_supermarket_df.to_dict(orient='records'),
        'worst': worst_supermarket_df.to_dict(orient='records')
    }


@app.post('/inflation')
async def calculate_inflation(shopping_list: List[Dict], date_range: List[str], session: Session = Depends(get_session)):
    start_date, end_date = date_range
    start_date, end_date = datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.strptime(end_date, '%Y-%m-%d').date()
    
    all_prods = []
    for prod in shopping_list:
        products = session.exec(
            select(Product).where(
                (Product.sku == prod['sku']) and ((Product.created_at == start_date) or (Product.created_at == end_date))
            ).order_by(Product.created_at.desc())
        ).all()

        all_prods += products
    
    inflation_df = pd.DataFrame.from_records([i.dict() for i in all_prods])
    inflation_df['created_at'] = pd.to_datetime(inflation_df['created_at']).dt.date
    
    inflation_by_date_df = inflation_df.groupby(by='created_at')['price'].agg(['min', 'max', 'mean']).reset_index()
    inflation_by_date_df['gap'] = inflation_by_date_df['max'] - inflation_by_date_df['min']

    # calculate average inflation
    start_mean = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == start_date, 'mean'].iloc[0]
    end_mean = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == end_date, 'mean'].iloc[0]
    mean_inflation = (end_mean - start_mean) / start_mean * 100
    
    # calculate lowest inflation
    start_min = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == start_date, 'min'].iloc[0]
    end_min = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == end_date, 'min'].iloc[0]
    min_inflation = (end_min - start_min) / start_min * 100

    # calculate gap inflation
    start_gap = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == start_date, 'gap'].iloc[0]
    end_gap = inflation_by_date_df.loc[inflation_by_date_df['created_at'] == end_date, 'gap'].iloc[0]
    gap_inflation = (end_gap - start_gap) / start_gap * 100

    return {
        'mean': round(mean_inflation, 2),
        'min': round(min_inflation, 2),
        'gap': round(gap_inflation, 2)
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)