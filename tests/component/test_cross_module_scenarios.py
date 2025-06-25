"""
Cross-module/component scenario tests for AI Toolkit for Small Business.
These tests simulate real-world workflows that span multiple modules.
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from operations import appointment_scheduler
from marketing import email_generator
from customer_service import sentiment_analysis

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

@pytest.mark.component
def test_booking_to_email_to_sentiment():
    """
    Scenario: A new booking is made, a confirmation email is generated, and the sentiment of the email is analyzed.
    This test ensures modules work together and handle realistic data.
    Skips if OpenAI API call fails (network, quota, etc).
    """
    # Step 1: Book an appointment (find available slot)
    working_hours = ("09:00", "17:00")
    bookings = []  # No existing bookings for this test
    slots = appointment_scheduler.get_available_slots(
        working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2025-07-01"
    )
    assert slots and isinstance(slots[0], tuple)
    slot = slots[0]
    booking = {
        "customer_name": "Jane Doe",
        "service": "Consultation",
        "date": slot[0],
        "time": slot[1],
        "location": "Main Office"
    }

    # Step 2: Generate confirmation email using function interface
    subject, plain, html = email_generator.generate_email(
        business_type="Consulting",
        offer_description=f"Appointment for {booking['service']} on {booking['date']} at {booking['time']} at {booking['location']}",
        tone="friendly"
    )
    assert isinstance(subject, str) and subject
    # If OpenAI API call failed, fail the test
    assert not plain.lower().startswith('[error]'), f"OpenAI API call failed: {plain}"
    # Check that the plain text email contains key appointment details (case-insensitive, robust to date/time formatting)
    assert booking["service"].lower() in plain.lower()
    # Accept any common natural date format (e.g., July 1, 2025, July 1st, 2025, or ISO)
    iso_date = booking["date"].lower()
    natural_date = "july 1, 2025"
    plain_lower = plain.lower()
    date_ok = (
        iso_date in plain_lower or
        natural_date in plain_lower or
        "july 1st, 2025" in plain_lower or
        ("july 1" in plain_lower and "2025" in plain_lower)
    )
    assert date_ok, f"Date not found in email body: {plain}"
    # Accept either 09:00 or 9:00 AM
    assert booking["time"] in plain or "9:00 am" in plain_lower
    assert booking["location"].lower() in plain_lower
    # Accept any non-empty HTML string (fragment or full document)
    assert isinstance(html, str) and len(html.strip()) > 0
    # Optionally, check that the date appears in the HTML as well
    assert "july 1" in html.lower() and "2025" in html.lower(), f"Date not found in HTML: {html}"

    # Step 3: Analyze sentiment of the plain text email using function interface
    sentiment_result = sentiment_analysis.analyze_sentiment(plain)
    assert isinstance(sentiment_result, dict)
    assert "sentiment" in sentiment_result
    assert sentiment_result["sentiment"] in ["positive", "neutral", "negative"]
