"""
Component/integration tests for AI for Small Business.
These tests use the real OpenAI API key and perform end-to-end checks.

To avoid accidental API usage, these tests are skipped if the API key is not set.
"""
import os
import pytest
from customer_service import chatbot

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_chatbot_faq_real_openai():
    # This test will use the real OpenAI API to answer a FAQ
    question = "What are your business hours?"
    answer = chatbot.ask_faq_bot(question)
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "hour" in answer.lower() or "open" in answer.lower()

def test_chatbot_api_real_openai():
    # This test will check the Flask API endpoint for the FAQ
    app = chatbot.app
    with app.test_client() as client:
        response = client.post("/faq", json={"question": "Where are you located?"})
        assert response.status_code == 200
        data = response.get_json()
        assert "answer" in data
        assert "location" in data["answer"].lower() or "address" in data["answer"].lower()

def test_chatbot_api_empty_question():
    # This test checks the API response for an empty question
    app = chatbot.app
    with app.test_client() as client:
        response = client.post("/faq", json={"question": ""})
        assert response.status_code == 200
        data = response.get_json()
        assert "answer" in data
        assert "sorry" in data["answer"].lower() or len(data["answer"]) > 0

def test_chatbot_faq_unknown_question():
    # This test checks the FAQ bot's response to an unknown question
    answer = chatbot.ask_faq_bot("What is the meaning of life?")
    assert isinstance(answer, str)
    assert len(answer) > 0
