"""
Test for customer_service/sentiment_analysis.py
"""
import pytest
from unittest.mock import patch
from customer_service import sentiment_analysis

def test_analyze_sentiment(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': '{"sentiment": "positive", "reasoning": "The text expresses satisfaction."}'})
        choices = [Choice()]
    monkeypatch.setattr(sentiment_analysis.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    result = sentiment_analysis.analyze_sentiment("Great service!")
    assert result["sentiment"] == "positive"
    assert "satisfaction" in result["reasoning"]
