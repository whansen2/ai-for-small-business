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
from typing import Optional
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.title("📊 Small Business KPI Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload KPI CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample data.")
    df = pd.DataFrame(read_csv("data/sample_kpi.csv"))

# Data processing
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

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
