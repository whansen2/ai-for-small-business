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
                self.message = type('msg', (), {'content': 'During the period from June 1 to June 2, 2024, the company recorded a total of 300 sales. On average, this amounted to 150 sales per day. The lowest number of sales in this period was 100, while the highest reached 200. Unfortunately, there is no sentiment data available for this period, making it difficult to assess customer moods or opinions regarding the service or products offered during these days.'})
        choices = [Choice()]
    monkeypatch.setattr(report_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    df = pd.DataFrame({"date": ["2024-06-01", "2024-06-02"], "sales": [100, 200]})
    summary = report_generator.summarize_with_openai(df)
    assert isinstance(summary, str) and len(summary) > 0
