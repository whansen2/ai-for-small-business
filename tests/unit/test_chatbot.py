"""
Test for customer_service/chatbot.py
"""
import pytest
from customer_service import chatbot


def test_ask_faq_bot(monkeypatch):
    monkeypatch.setattr(
        chatbot, "ask_faq_bot", lambda q: "We are open Monday to Friday, 9am to 6pm."
    )
    answer = chatbot.ask_faq_bot("What are your business hours?")
    assert "Monday to Friday" in answer
