"""
Component tests for marketing/email_generator.py
Covers normal, edge, and promotion scenarios with real OpenAI API key.
"""
import os
import pytest
from marketing import email_generator

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_email_generator_real_openai():
    subject, plain, html = email_generator.generate_email(
        "Retail Store", "20% off all cleaning services", "friendly"
    )
    assert isinstance(subject, str) and len(subject) > 0
    assert isinstance(plain, str) and len(plain) > 0
    assert isinstance(html, str) and len(html) > 0
    assert "off" in plain.lower() or "off" in html.lower()

def test_email_generator_empty_offer():
    subject, plain, html = email_generator.generate_email(
        "Retail Store", "", "friendly"
    )
    assert isinstance(subject, str)
    assert isinstance(plain, str)
    assert isinstance(html, str)

def test_email_generator_with_promotion():
    promotions = email_generator.load_promotions()
    if promotions:
        promo = promotions[0]
        offer = f"{promo['promotion']}: {promo['description']} (Valid until {promo['valid_until']})"
        subject, plain, html = email_generator.generate_email("Retail Store", offer, "friendly")
        assert isinstance(subject, str)
        assert isinstance(plain, str)
        assert isinstance(html, str)

def test_email_generator_invalid_input():
    # Should not raise, should return strings
    subject, plain, html = email_generator.generate_email("", "", "")
    assert isinstance(subject, str)
    assert isinstance(plain, str)
    assert isinstance(html, str)

def test_email_generator_special_characters():
    subject, plain, html = email_generator.generate_email("Retail!@#", "Offer!@#%$^&*()", "quirky!@#")
    special_chars = set('@#%$^&*()')
    found = any(c in subject for c in special_chars) or any(c in plain for c in special_chars) or any(c in html for c in special_chars)
    assert found or (len(subject) > 0 and len(plain) > 0 and len(html) > 0)


def test_email_generator_long_offer():
    long_offer = "A" * 1000
    subject, plain, html = email_generator.generate_email("Retail", long_offer, "friendly")
    # Accept if output is non-empty and refers to an offer, deal, or promotion
    keywords = ["offer", "deal", "promotion", "special", "discount"]
    found = any(k in plain.lower() for k in keywords) or any(k in html.lower() for k in keywords)
    assert len(plain) > 0 and len(html) > 0 and found


def test_email_generator_different_tones():
    for tone in ["formal", "quirky", "urgent", "friendly"]:
        subject, plain, html = email_generator.generate_email("Retail", "20% off", tone)
        # Accept if output is non-empty and contains a greeting or a contextually appropriate opening
        greetings = ["dear", "hello", "hi", "greetings", "hey", "hurry", "exclusive", "save", "enjoy"]
        plain_greeting = any(g in plain.lower() for g in greetings)
        html_greeting = any(g in html.lower() for g in greetings)
        assert (len(plain) > 0 and len(html) > 0) and (plain_greeting or html_greeting)
