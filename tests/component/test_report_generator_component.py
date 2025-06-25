"""
Component tests for automation/report_generator.py
Covers normal, missing sentiment, and PDF output scenarios.
"""
import os
import pytest
from automation import report_generator

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_report_generator_real_pdf():
    out_pdf = "test_business_report.pdf"
    report_generator.generate_pdf_report(
        sales_csv="data/sample_sales_month.csv",
        sentiment_csv=None,
        out_pdf=out_pdf
    )
    assert os.path.exists(out_pdf)
    assert os.path.getsize(out_pdf) > 0
    os.remove(out_pdf)

def test_report_generator_missing_sentiment():
    out_pdf = "test_business_report_no_sentiment.pdf"
    report_generator.generate_pdf_report(
        sales_csv="data/sample_sales.csv",
        sentiment_csv=None,
        out_pdf=out_pdf
    )
    assert os.path.exists(out_pdf)
    os.remove(out_pdf)
