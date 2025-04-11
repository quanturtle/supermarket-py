from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

import os
import uvicorn
import pandas as pd
from sqlmodel import Session, select, or_
from sqlalchemy import func, desc, over
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from models import Product, get_session


app = FastAPI(
    title='supermarket-py-backend',
    description='API for comparing prices of products across different supermarkets',
    version='1.0.0',
)

if os.getenv('IS_PROD', 'True') == 'True':
    origins = [
        os.getenv('FRONTEND_URL')
    ]
else:
    origins = [
        '*'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


@app.get('/health', status_code=status.HTTP_200_OK)
async def get_catalog(session: Session = Depends(get_session)):
    return {'status': 'ok'}


@app.get('/catalog')
async def get_catalog(session: Session = Depends(get_session)):
    query = select(Product.id, Product.name, Product.sku).distinct(Product.sku)
    return session.exec(query).mappings().all()


@app.get('/product/{product_sku}')
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
    
    if not price_history:
        return {
            'history': '',
            'product_info': {
                'name': '', 
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
            'name': latest_product_prices_df.iloc[0]['name'], 
            'sku': product_sku
        },
        'price_changes': product_price_changes
    }


@app.get('/products/search/')
async def search_products(query: str, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product.id, Product.name, Product.sku).distinct(Product.sku) \
            .where(
                (Product.name.ilike(f'%{query}%'))
            ).limit(5)
    ).mappings().all()
    
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


def compute_global_inflation(inflation_df: pd.DataFrame, start_date: datetime, end_date: datetime) -> Dict:
    # group by and compute gap
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
        'mean_inflation': {
            'start_price': round(start_mean, 2),
            'end_price': round(end_mean, 2),
            'absolute_change': round(abs(end_mean - start_mean), 2),
            'inflation_rate': round(mean_inflation, 2)
        },
        'min_inflation': {
            'start_price': round(start_min, 2),
            'end_price': round(end_min, 2),
            'absolute_change': round(abs(end_min - start_min), 2),
            'inflation_rate': round(min_inflation, 2)
        },
        'gap_inflation': {
            'start_price': round(start_gap, 2),
            'end_price': round(end_gap, 2),
            'absolute_change': round(abs(end_gap - start_gap), 2),
            'inflation_rate': round(gap_inflation, 2)
        }
    }


def compute_per_product_inflation(inflation_df: pd.DataFrame, start_date: datetime, end_date: datetime): #-> List[Dict]:
    unique_skus = inflation_df['sku'].unique()

    results = []
    
    for sku in unique_skus:
        product_df = inflation_df[inflation_df['sku']==sku]
        product_name = product_df['name'].iloc[0]

        start_avg_price = product_df[product_df['created_at'] == start_date]['price'].mean()
        end_avg_price = product_df[product_df['created_at'] == end_date]['price'].mean()

        if start_avg_price > 0:  # Avoid division by zero
            inflation_rate = ((end_avg_price - start_avg_price) / start_avg_price) * 100
        else:
            inflation_rate = 0

        results.append({
            'sku': sku,
            'name': product_name,
            'inflation_rate': round(inflation_rate, 2)
        })

    return results


@app.post('/inflation')
async def calculate_inflation(shopping_list: List[Dict], date_range: List[str], session: Session = Depends(get_session)):
    start_date, end_date = date_range
    start_date, end_date = datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.strptime(end_date, '%Y-%m-%d').date()
    
    skus = [prod['sku'] for prod in shopping_list]
    
    all_prods = session.exec(
        select(Product).where(Product.sku.in_(skus)).where(
            or_(
                func.date(Product.created_at) == start_date, 
                func.date(Product.created_at) == end_date
            )
        )
    ).all()
    
    inflation_df = pd.DataFrame.from_records([dict(i) for i in all_prods])
    inflation_df['created_at'] = pd.to_datetime(inflation_df['created_at']).dt.date
    
    global_inflation = compute_global_inflation(inflation_df, start_date, end_date)
    per_product_inflation = compute_per_product_inflation(inflation_df, start_date, end_date)
    
    return {
        'global_inflation': global_inflation,
        'per_product_inflation': per_product_inflation
    }
    
@app.get('/inflation/date-range')
async def available_date_range(session: Session = Depends(get_session)):
    date_range = session.exec(
        select(
            func.min(Product.created_at),
            func.max(Product.created_at)
        )
    ).mappings().first()
    
    return {
        'start_date': date_range['min'].date(),
        'end_date': date_range['max'].date()
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)