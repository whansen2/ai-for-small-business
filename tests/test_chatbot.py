"""
Test for customer_service/chatbot.py
"""
import pytest
from unittest.mock import patch
from customer_service import chatbot

def test_ask_faq_bot(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': 'We are open Monday to Friday, 9am to 6pm.'})
        choices = [Choice()]
    monkeypatch.setattr(chatbot.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    answer = chatbot.ask_faq_bot("What are your business hours?")
    assert "Monday to Friday" in answer
