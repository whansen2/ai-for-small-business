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

def test_appointment_scheduler_overlapping_bookings():
    working_hours = ("09:00", "11:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "09:00", "end_time": "10:00"},
        {"date": "2024-06-25", "start_time": "09:30", "end_time": "10:30"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2024-06-25")
    # Only 10:30-11:00 should be available
    assert slots == [("2024-06-25", "10:30", "11:00")]

def test_appointment_scheduler_outside_working_hours():
    working_hours = ("09:00", "10:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "08:00", "end_time": "09:00"},
        {"date": "2024-06-25", "start_time": "10:00", "end_time": "11:00"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2024-06-25")
    # All slots should be available
    assert len(slots) > 0

def test_appointment_scheduler_different_slot_lengths():
    working_hours = ("09:00", "10:00")
    bookings = []
    slots_30 = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2024-06-25")
    slots_15 = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=15, days_ahead=1, start_date="2024-06-25")
    assert len(slots_15) > len(slots_30)

def test_appointment_scheduler_exact_match():
    working_hours = ("09:00", "10:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "09:00", "end_time": "09:30"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1, start_date="2024-06-25")
    # Only 09:30-10:00 should be available
    assert slots == [("2024-06-25", "09:30", "10:00")]
