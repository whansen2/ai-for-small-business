"""
Test for operations/appointment_scheduler.py
"""
import pytest
from operations import appointment_scheduler

def test_get_available_slots():
    bookings = [
        {"date": "2025-06-25", "start_time": "09:00", "end_time": "09:30"},
        {"date": "2025-06-25", "start_time": "10:00", "end_time": "10:30"}
    ]
    slots = appointment_scheduler.get_available_slots(("09:00", "12:00"), bookings, slot_minutes=30, days_ahead=1)
    # Should not overlap with booked slots
    for s in slots:
        for b in bookings:
            assert not (s[0] == b["date"] and s[1] == b["start_time"] and s[2] == b["end_time"])
