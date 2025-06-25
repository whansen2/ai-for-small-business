"""
Test for operations/invoice_processor.py
"""
import pytest
from operations import invoice_processor
import tempfile
import os

def test_extract_fields():
    text = "Vendor: Acme Supplies\nDate: 2024-01-15\nTotal Amount: $1,250.00"
    fields = invoice_processor.extract_fields(text)
    assert fields["vendor"] == "Acme Supplies"
    assert fields["date"] == "2024-01-15"
    assert fields["total_amount"] == "1,250.00"
