"""
Streamlit KPI Dashboard for Small Business Analytics
- Displays revenue trends, customer growth, conversion rates
- Allows CSV upload
- Option to export dashboard as PDF
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_io import read_csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv

st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.title("📊 Small Business KPI Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload KPI CSV", type=["csv"])

def load_sentiment_summary(sentiment_csv: str = "data/sample_sales_month.csv") -> str:
    try:
        with open(sentiment_csv, mode='r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
            sentiments = [r.get('customer_sentiment', '') for r in rows if 'customer_sentiment' in r]
            if sentiments:
                from collections import Counter
                top = Counter(sentiments).most_common(1)[0][0]
                return f"Top customer sentiment: {top}"
    except Exception:
        pass
    return "Sentiment data unavailable."

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample data.")
    df = pd.DataFrame(read_csv("data/sample_kpi.csv"))

# Data processing
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    # Ensure numeric columns are properly converted
    for col in ['revenue', 'customers', 'conversions']:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.sort_values('date')

    # Metrics
    avg_order_value = df['revenue'].mean() if 'revenue' in df else None
    best_sales_day = df.loc[df['revenue'].idxmax(), 'date'].strftime('%Y-%m-%d') if 'revenue' in df else None
    st.metric("Average Revenue", f"${avg_order_value:,.2f}" if avg_order_value else "N/A")
    st.metric("Best Sales Day", best_sales_day if best_sales_day else "N/A")
    sentiment_summary = load_sentiment_summary()
    st.info(sentiment_summary)

    # Revenue trend, Customer growth, and Conversion rates in columns
    st.subheader("KPI Trends")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Revenue Trend")
        fig1, ax1 = plt.subplots(figsize=(4, 2))
        ax1.plot(df['date'], df['revenue'], marker='o', color='#0072B5', linewidth=1.5)
        ax1.set_xlabel('Date', fontsize=8)
        ax1.set_ylabel('Revenue', fontsize=8)
        ax1.set_title('Revenue Over Time', fontsize=10, fontweight='bold')
        ax1.grid(True, linestyle='--', alpha=0.5)
        fig1.tight_layout()
        fig1.autofmt_xdate(rotation=30, ha='right')
        st.pyplot(fig1)

    with col2:
        st.caption("Customer Growth")
        fig2, ax2 = plt.subplots(figsize=(4, 2))
        ax2.plot(df['date'], df['customers'], marker='o', color='#3CB371', linewidth=1.5)
        ax2.set_xlabel('Date', fontsize=8)
        ax2.set_ylabel('Customers', fontsize=8)
        ax2.set_title('Customer Growth', fontsize=10, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.5)
        fig2.tight_layout()
        fig2.autofmt_xdate(rotation=30, ha='right')
        st.pyplot(fig2)

    with col3:
        st.caption("Conversion Rates")
        fig3, ax3 = plt.subplots(figsize=(4, 2))
        ax3.plot(df['date'], df['conversions'], marker='o', color='#FFA500', linewidth=1.5)
        ax3.set_xlabel('Date', fontsize=8)
        ax3.set_ylabel('Conversions', fontsize=8)
        ax3.set_title('Conversion Rates', fontsize=10, fontweight='bold')
        ax3.grid(True, linestyle='--', alpha=0.5)
        fig3.tight_layout()
        fig3.autofmt_xdate(rotation=30, ha='right')
        st.pyplot(fig3)

    # Export as PDF
    if st.button("Export Dashboard as PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "KPI Dashboard Report")
        c.drawString(100, 730, f"Revenue (last): {df['revenue'].iloc[-1]}")
        c.drawString(100, 710, f"Customers (last): {df['customers'].iloc[-1]}")
        c.drawString(100, 690, f"Conversions (last): {df['conversions'].iloc[-1]}")
        c.drawString(100, 670, f"Average Revenue: ${avg_order_value:,.2f}" if avg_order_value else "")
        c.drawString(100, 650, f"Best Sales Day: {best_sales_day}" if best_sales_day else "")
        c.drawString(100, 630, sentiment_summary)
        c.save()
        buffer.seek(0)
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="kpi_dashboard.pdf",
            mime="application/pdf"
        )
else:
    st.warning("No data to display.")
