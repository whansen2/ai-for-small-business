"""
Component tests for operations/invoice_processor.py
Covers normal, missing field, and malformed invoice scenarios.
"""
import os
import pytest
from operations import invoice_processor

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_invoice_processor_real_sample():
    sample_path = "data/invoices/sample_invoice.txt"
    fields = invoice_processor.process_invoice_file(sample_path)
    assert fields["vendor"] == "Acme Supplies"
    assert fields["date"] == "2024-01-15"
    assert fields["total_amount"] == "1,250.00"

def test_invoice_processor_missing_field():
    text = "Vendor: Acme Supplies\nTotal Amount: $1,250.00"
    fields = invoice_processor.extract_fields(text)
    assert fields["vendor"] == "Acme Supplies"
    assert fields["date"] == ""
    assert fields["total_amount"] == "1,250.00"

def test_invoice_processor_malformed():
    text = "Random text with no fields"
    fields = invoice_processor.extract_fields(text)
    assert fields["vendor"] == ""
    assert fields["date"] == ""
    assert fields["total_amount"] == ""
