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


def test_generate_email_empty_offer(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "No Offer", "plain": "No offer available.", "html": "<b>No offer</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "", "friendly")
    assert isinstance(subject, str) and len(subject) > 0
    assert isinstance(plain, str) and len(plain) > 0
    assert isinstance(html, str) and len(html) > 0


def test_generate_email_special_characters(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "Special! @#%$^&*()", "plain": "Special chars: @#%$^&*()", "html": "<b>Special chars: @#%$^&*()</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "@#%$^&*()", "friendly")
    special_chars = set('@#%$^&*()')
    found = any(c in subject for c in special_chars) or any(c in plain for c in special_chars) or any(c in html for c in special_chars)
    assert found or (len(subject) > 0 and len(plain) > 0 and len(html) > 0)


def test_generate_email_long_offer(monkeypatch):
    long_offer = "A" * 1000

    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "Long Offer", "plain": "' + long_offer + '", "html": "<b>' + long_offer + '</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", long_offer, "friendly")
    keywords = ["offer", "deal", "promotion", "special", "discount"]
    found = any(k in plain.lower() for k in keywords) or any(k in html.lower() for k in keywords)
    assert len(plain) > 0 and len(html) > 0 and found


def test_generate_email_different_tones(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "Formal", "plain": "Dear Customer,", "html": "<b>Dear Customer,</b>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "20% off", "formal")
    greetings = ["dear", "hello", "hi", "greetings"]
    plain_greeting = any(g in plain.lower() for g in greetings)
    html_greeting = any(g in html.lower() for g in greetings)
    assert plain_greeting or html_greeting


def test_generate_email_html_valid(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": '{"subject": "HTML", "plain": "Plain.", "html": "<html><body><b>HTML</b></body></html>"}'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse()
    )
    subject, plain, html = email_generator.generate_email("Retail", "20% off", "friendly")
    assert html.startswith("<html>") or "<b>" in html


def test_generate_email_malformed_response(monkeypatch):
    class MockResponse:
        class Choice:
            def __init__(self):
                self.message = type(
                    "msg",
                    (),
                    {
                        "content": 'not a json string'
                    },
                )

        choices = [Choice()]

    monkeypatch.setattr(
        email_generator.openai.ChatCompletion, "create", lambda *a, **kw: MockResponse())
    subject, plain, html = email_generator.generate_email("Retail", "20% off", "friendly")
    assert isinstance(subject, str)
    assert isinstance(plain, str)
    assert isinstance(html, str)
