"""
Test for automation/report_generator.py
"""
import pytest
from unittest.mock import patch
from automation import report_generator
import pandas as pd

def test_summarize_with_openai(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': 'Sales increased by 12% in June.'})
        choices = [Choice()]
    monkeypatch.setattr(report_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    df = pd.DataFrame({"date": ["2024-06-01", "2024-06-02"], "sales": [100, 200]})
    summary = report_generator.summarize_with_openai(df)
    assert "Sales increased" in summary
