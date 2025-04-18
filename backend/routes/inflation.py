from typing import List, Dict
from datetime import datetime
import pandas as pd
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, or_
from sqlalchemy import func
from models import Product, Supermarket, get_session


router = APIRouter(prefix="", tags=["inflation"])
inflation_router = router


def compute_global_inflation(inflation_df: pd.DataFrame, start_date: datetime, end_date: datetime):
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


def compute_per_product_inflation(inflation_df: pd.DataFrame, start_date: datetime, end_date: datetime):
    unique_skus = inflation_df['sku'].unique()

    results = []
    
    for sku in unique_skus:
        product_df = inflation_df[inflation_df['sku']==sku]
        product_description = product_df['description'].iloc[0]

        start_avg_price = product_df[product_df['created_at'] == start_date]['price'].mean()
        end_avg_price = product_df[product_df['created_at'] == end_date]['price'].mean()

        if start_avg_price > 0:  # Avoid division by zero
            inflation_rate = ((end_avg_price - start_avg_price) / start_avg_price) * 100
        else:
            inflation_rate = 0

        results.append({
            'sku': sku,
            'description': product_description,
            'inflation_rate': round(inflation_rate, 2)
        })

    return results


@router.post('/inflation')
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


@router.get('/inflation/date-range')
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