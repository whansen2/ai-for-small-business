"""
Test for analytics/sales_forecast.py
"""
import pytest
from analytics import sales_forecast
import pandas as pd

def test_load_sales_data():
    df = sales_forecast.load_sales_data("data/sample_sales.csv")
    assert not df.empty
    assert 'date' in df.columns
    assert 'sales' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_numeric_dtype(df['sales'])
