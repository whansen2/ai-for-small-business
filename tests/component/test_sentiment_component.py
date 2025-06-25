"""
Component tests for customer_service/sentiment_analysis.py
Covers positive, negative, and empty input scenarios with real OpenAI API key.
"""
import os
import pytest
from customer_service import sentiment_analysis

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_sentiment_analysis_positive():
    text = "The staff was very helpful and friendly."
    result = sentiment_analysis.analyze_sentiment(text)
    assert result["sentiment"] == "positive"
    assert "reasoning" in result

def test_sentiment_analysis_negative():
    text = "I am very disappointed with the service."
    result = sentiment_analysis.analyze_sentiment(text)
    assert result["sentiment"] == "negative"
    assert "reasoning" in result

def test_sentiment_analysis_empty():
    text = ""
    result = sentiment_analysis.analyze_sentiment(text)
    assert result["sentiment"] in ["neutral", "negative", "positive"]
    assert "reasoning" in result
