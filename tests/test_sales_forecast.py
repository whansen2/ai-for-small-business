"""
Test for analytics/sales_forecast.py
"""
import pytest
from analytics import sales_forecast
import pandas as pd

def test_load_sales_data(tmp_path):
    # Create a sample CSV
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("date,sales\n2024-01-01,100\n2024-01-02,200\n")
    df = sales_forecast.load_sales_data(str(csv_path))
    assert not df.empty
    assert list(df.columns) == ["date", "sales"]
    assert df["sales"].sum() == 300
