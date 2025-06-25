"""
Sales Forecasting from historical CSV data using Prophet, ARIMA, and Linear Regression.
Generates and saves forecast plots using matplotlib.
- Robust to missing dependencies (Prophet, ARIMA)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
from utils.file_io import read_csv
from sklearn.linear_model import LinearRegression

# Prophet
try:
    from prophet import Prophet
except ImportError:
    Prophet = None
# ARIMA
try:
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:
    ARIMA = None


def load_sales_data(csv_path: str) -> pd.DataFrame:
    """Load sales data from CSV."""
    df = pd.DataFrame(read_csv(csv_path))
    df['date'] = pd.to_datetime(df['date'])
    df['sales'] = pd.to_numeric(df['sales'])
    return df

def forecast_prophet(df: pd.DataFrame, periods: int = 7) -> Tuple[pd.DataFrame, str]:
    if Prophet is None:
        raise ImportError("Prophet is not installed.")
    prophet_df = df.rename(columns={'date': 'ds', 'sales': 'y'})
    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    fig = model.plot(forecast)
    plot_path = "prophet_forecast.png"
    fig.savefig(plot_path)
    return forecast[['ds', 'yhat']], plot_path

def forecast_arima(df: pd.DataFrame, periods: int = 7) -> Tuple[np.ndarray, str]:
    if ARIMA is None:
        raise ImportError("statsmodels is not installed.")
    model = ARIMA(df['sales'], order=(1,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=periods)
    plt.figure()
    plt.plot(df['date'], df['sales'], label='History')
    plt.plot(pd.date_range(df['date'].iloc[-1], periods=periods+1, freq='D')[1:], forecast, label='ARIMA Forecast')
    plt.legend()
    plot_path = "arima_forecast.png"
    plt.savefig(plot_path)
    return forecast, plot_path

def forecast_linear_regression(df: pd.DataFrame, periods: int = 7) -> Tuple[np.ndarray, str]:
    df = df.copy()
    df['ordinal'] = df['date'].map(pd.Timestamp.toordinal)
    X = df['ordinal'].values.reshape(-1, 1)
    y = df['sales'].values
    model = LinearRegression()
    model.fit(X, y)
    future_dates = [df['date'].iloc[-1] + pd.Timedelta(days=i) for i in range(1, periods+1)]
    X_future = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    forecast = model.predict(X_future)
    plt.figure()
    plt.plot(df['date'], y, label='History')
    plt.plot(future_dates, forecast, label='Linear Regression Forecast')
    plt.legend()
    plot_path = "linear_regression_forecast.png"
    plt.savefig(plot_path)
    return forecast, plot_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sales Forecasting")
    parser.add_argument("--csv", required=True, type=str, help="Path to sales CSV file")
    parser.add_argument("--periods", type=int, default=7, help="Forecast periods (days)")
    args = parser.parse_args()
    df = load_sales_data(args.csv)
    print("Running Prophet forecast...")
    try:
        prophet_forecast, prophet_plot = forecast_prophet(df, args.periods)
        print(f"Prophet forecast plot saved to {prophet_plot}")
    except Exception as e:
        print(f"Prophet error: {e}")
    print("Running ARIMA forecast...")
    try:
        arima_forecast, arima_plot = forecast_arima(df, args.periods)
        print(f"ARIMA forecast plot saved to {arima_plot}")
    except Exception as e:
        print(f"ARIMA error: {e}")
    print("Running Linear Regression forecast...")
    try:
        lr_forecast, lr_plot = forecast_linear_regression(df, args.periods)
        print(f"Linear Regression forecast plot saved to {lr_plot}")
    except Exception as e:
        print(f"Linear Regression error: {e}")

if __name__ == "__main__":
    main()
