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

def test_summarize_with_sentiment(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': 'Between June 1 and June 2, 2024, sales totaled 300. Sentiment was positive.'})
        choices = [Choice()]
    monkeypatch.setattr(report_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    df = pd.DataFrame({"date": ["2024-06-01", "2024-06-02"], "sales": [100, 200], "customer_sentiment": ["positive", "positive"]})
    summary = report_generator.summarize_with_openai(df)
    assert "sentiment" in summary.lower()

def test_summarize_with_openai_malformed(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': ''})
        choices = [Choice()]
    monkeypatch.setattr(report_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    df = pd.DataFrame({"date": ["2024-06-01", "2024-06-02"], "sales": [100, 200]})
    summary = report_generator.summarize_with_openai(df)
    assert isinstance(summary, str)

def test_summarize_with_openai_relevance(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': 'Total sales: 300. Average: 150.'})
        choices = [Choice()]
    monkeypatch.setattr(report_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    df = pd.DataFrame({"date": ["2024-06-01", "2024-06-02"], "sales": [100, 200]})
    summary = report_generator.summarize_with_openai(df)
    assert "300" in summary or "150" in summary
