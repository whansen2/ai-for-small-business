"""
Component tests for operations/appointment_scheduler.py
Covers normal, fully booked, and empty bookings scenarios.
"""
import os
import pytest
from operations import appointment_scheduler

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_appointment_scheduler_real_openai():
    working_hours = ("09:00", "17:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "09:00", "end_time": "09:30"},
        {"date": "2024-06-25", "start_time": "10:00", "end_time": "10:30"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1)
    assert isinstance(slots, list)
    formatted = appointment_scheduler.format_slots_human(slots)
    assert isinstance(formatted, str)
    assert "appointment" in formatted.lower() or "slot" in formatted.lower() or len(formatted) > 0

def test_appointment_scheduler_fully_booked():
    working_hours = ("09:00", "10:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "09:00", "end_time": "09:30"},
        {"date": "2024-06-25", "start_time": "09:30", "end_time": "10:00"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2024-06-25")
    assert slots == []

def test_appointment_scheduler_empty_bookings():
    working_hours = ("09:00", "10:00")
    bookings = []
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1)
    assert len(slots) > 0
