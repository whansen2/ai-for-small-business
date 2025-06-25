"""
Test for marketing/email_generator.py
"""
import pytest
from marketing import email_generator


def test_generate_email(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "Sale!", "plain": "Plain text.", "html": "<b>HTML</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "20% off", "friendly")
    assert subject == "Sale!"
    assert "Plain text" in plain
    assert "<b>HTML</b>" in html
