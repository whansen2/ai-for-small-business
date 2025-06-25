"""
Test for marketing/email_generator.py
"""
import pytest
from unittest.mock import patch
from marketing import email_generator

def test_generate_email(monkeypatch):
    # Mock OpenAI response
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type('msg', (), {'content': '{"subject": "Test Subject", "plain": "Test plain body.", "html": "<p>Test HTML body.</p>"}'})
        choices = [Choice()]
    monkeypatch.setattr(email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    subject, plain, html = email_generator.generate_email("Retail Store", "20% off sale", "friendly")
    assert subject == "Test Subject"
    assert "plain" in plain or "Test plain body." in plain
    assert "<p>Test HTML body.</p>" in html
