"""
Monthly Business PDF Report Generator
- Pulls sales data from CSV
- Pulls customer sentiment from text or CSV
- Uses OpenAI to write narrative summaries
- Combines with plots into PDF using reportlab
"""
import openai
import pandas as pd
import matplotlib.pyplot as plt
from utils.config import OPENAI_API_KEY
from utils.file_io import read_csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import Optional
import os

openai.api_key = OPENAI_API_KEY

SUMMARY_PROMPT = (
    "You are a business analyst. Given sales and sentiment data, write a narrative summary (e.g., 'Sales increased by 12%...')."
)

def load_data(sales_csv: str, sentiment_csv: Optional[str] = None) -> pd.DataFrame:
    sales = pd.DataFrame(read_csv(sales_csv))
    sales['date'] = pd.to_datetime(sales['date'])
    sales['sales'] = pd.to_numeric(sales['sales'])
    if sentiment_csv:
        sentiment = pd.DataFrame(read_csv(sentiment_csv))
        sales = sales.merge(sentiment, on='date', how='left')
    return sales

def plot_sales(df: pd.DataFrame, out_path: str) -> None:
    plt.figure()
    plt.plot(df['date'], df['sales'], marker='o')
    plt.title('Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def summarize_with_openai(df: pd.DataFrame) -> str:
    sales_stats = {
        'total_sales': df['sales'].sum(),
        'avg_sales': df['sales'].mean(),
        'min_sales': df['sales'].min(),
        'max_sales': df['sales'].max(),
        'period': f"{df['date'].min().date()} to {df['date'].max().date()}"
    }
    sentiment_counts = df['customer_sentiment'].value_counts().to_dict() if 'customer_sentiment' in df else {}
    prompt = f"Sales stats: {sales_stats}\nSentiment counts: {sentiment_counts}"
    messages = [
        {"role": "system", "content": SUMMARY_PROMPT},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

def generate_pdf_report(sales_csv: str, sentiment_csv: Optional[str], out_pdf: str) -> None:
    df = load_data(sales_csv, sentiment_csv)
    plot_path = "sales_plot.png"
    plot_sales(df, plot_path)
    summary = summarize_with_openai(df)
    c = canvas.Canvas(out_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, "Monthly Business Report")
    c.setFont("Helvetica", 12)
    c.drawString(72, 730, summary)
    c.drawImage(plot_path, 72, 500, width=400, height=200)
    c.save()
    os.remove(plot_path)
    print(f"PDF report saved to {out_pdf}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Monthly Business Report Generator")
    parser.add_argument("--sales_csv", type=str, default="data/sample_sales_month.csv", help="Sales CSV file")
    parser.add_argument("--sentiment_csv", type=str, help="Optional: customer sentiment CSV file")
    parser.add_argument("--out_pdf", type=str, default="business_report.pdf", help="Output PDF file")
    args = parser.parse_args()
    generate_pdf_report(args.sales_csv, args.sentiment_csv, args.out_pdf)

if __name__ == "__main__":
    main()
