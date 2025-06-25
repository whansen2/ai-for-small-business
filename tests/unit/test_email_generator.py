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
                        "content": '{"subject": "🎉 Big Savings Alert! 20% Off Just for You! 🎈", "plain": "Hi there!\n\nWe\'re excited to offer you a special treat! Shop now and enjoy 20% off your next purchase. It\'s our way of saying thanks for being such a wonderful customer.\n\nSimply use code SAVE20 at checkout and watch the savings add up! Whether it\'s a new outfit, your favorite gadget, or home essentials, we\'ve got you covered.\n\nDon’t miss out on this limited-time offer! Head over to our store and grab your favorites.\n\nSee you soon!\n\nCheers,\nYour Retail Family", "html": "<b>HTML</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "20% off", "friendly")
    assert isinstance(subject, str) and len(subject) > 0
    assert isinstance(plain, str) and len(plain) > 0
    assert isinstance(html, str) and len(html) > 0
