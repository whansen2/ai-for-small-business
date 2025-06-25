"""
Test for operations/appointment_scheduler.py
"""
import pytest
from operations import appointment_scheduler

def test_get_available_slots():
    working_hours = ("09:00", "17:00")
    bookings = [
        {"date": "2024-06-25", "start_time": "09:00", "end_time": "09:30"},
        {"date": "2024-06-25", "start_time": "10:00", "end_time": "10:30"}
    ]
    slots = appointment_scheduler.get_available_slots(working_hours, bookings, slot_minutes=30, days_ahead=1)
    assert isinstance(slots, list)
    assert all(len(slot) == 3 for slot in slots)
