"""
Component/integration tests for AI for Small Business.
These tests use the real OpenAI API key and perform end-to-end checks.

To avoid accidental API usage, these tests are skipped if the API key is not set.
"""
import os
import pytest
import openai
from customer_service import chatbot

def has_api_key():
    return bool(os.getenv("OPENAI_API_KEY"))

pytestmark = pytest.mark.skipif(not has_api_key(), reason="No OpenAI API key set.")

def test_chatbot_real_openai():
    # This test will use the real OpenAI API to answer a FAQ
    question = "What are your business hours?"
    answer = chatbot.get_answer(question)
    assert isinstance(answer, str)
    assert len(answer) > 0
