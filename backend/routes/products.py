from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, or_
from sqlalchemy import func, desc
from models import Product, Supermarket, get_session


router = APIRouter(prefix="", tags=["products"])
products_router = router


@router.get('/product/{product_sku}')
async def get_product_by_sku(product_sku: str, session: Session = Depends(get_session)):
    seven_days_ago = datetime.today().date() - timedelta(days=7)

    price_history_stmt = (
        select(
            Product.supermarket_id,
            Product.description,
            Product.price,
            Product.created_at
        )
        .where(Product.sku == product_sku)
        .where(seven_days_ago <= Product.created_at)
    )
    
    price_history = session.exec(price_history_stmt).all()
    
    if not price_history:
        return {
            'history': '',
            'product_info': {
                'description': '', 
                'sku': ''
            },
            'price_changes': ''
        }
    
    latest_product_prices_df = pd.DataFrame(price_history).sort_values(by=['supermarket_id', 'created_at'], ascending=[True, True])

    product_price_changes = []
    
    for supermarket_id, group in latest_product_prices_df.groupby('supermarket_id'):
        start_date_price = group[group['created_at'] == group['created_at'].min()]['price'].values[0]
        end_date_price = group[group['created_at'] == group['created_at'].max()]['price'].values[0]
        
        # avoid division by zero
        if start_date_price > 0:  
            pct_change = ((end_date_price - start_date_price) / start_date_price) * 100
        else:
            pct_change = 0
            
        # create record for this supermarket's price change
        price_change_record = {
            'supermarket_id': supermarket_id,
            'price': start_date_price,
            'pct_change': round(pct_change, 2)
        }
        
        product_price_changes.append(price_change_record)

    return {
        'history': latest_product_prices_df.to_dict(orient='records'),
        'product_info': {
            'description': latest_product_prices_df.iloc[0]['description'], 
            'sku': product_sku
        },
        'price_changes': product_price_changes
    }


@router.get('/products/search/')
async def search_products(query: str, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product.id, Product.description, Product.sku).distinct(Product.sku) \
            .where(
                (Product.description.ilike(f'%{query}%'))
            ).limit(5)
    ).mappings().all()
    
    return products


@router.post('/price-comparison')
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
                Product.description,
                Product.sku,
                Product.price,
                Product.url,
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
                subquery.c.description,
                subquery.c.sku,
                subquery.c.price,
                subquery.c.url,
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