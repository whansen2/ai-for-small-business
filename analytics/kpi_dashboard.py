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
    df = df.sort_values('date')

    # Metrics
    avg_order_value = df['revenue'].mean() if 'revenue' in df else None
    best_sales_day = df.loc[df['revenue'].idxmax(), 'date'].strftime('%Y-%m-%d') if 'revenue' in df else None
    st.metric("Average Revenue", f"${avg_order_value:,.2f}" if avg_order_value else "N/A")
    st.metric("Best Sales Day", best_sales_day if best_sales_day else "N/A")
    sentiment_summary = load_sentiment_summary()
    st.info(sentiment_summary)

    # Revenue trend
    st.subheader("Revenue Trend")
    fig1, ax1 = plt.subplots()
    ax1.plot(df['date'], df['revenue'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Revenue')
    st.pyplot(fig1)

    # Customer growth
    st.subheader("Customer Growth")
    fig2, ax2 = plt.subplots()
    ax2.plot(df['date'], df['customers'], marker='o', color='green')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Customers')
    st.pyplot(fig2)

    # Conversion rates
    st.subheader("Conversion Rates")
    fig3, ax3 = plt.subplots()
    ax3.plot(df['date'], df['conversions'], marker='o', color='orange')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Conversions')
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
