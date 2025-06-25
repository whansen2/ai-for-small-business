"""
Test for automation/inventory_tracker.py
"""
import pytest
from automation import inventory_tracker

def test_get_restock_items():
    inventory = [
        {"item": "Printer Paper", "stock": "5", "threshold": "10"},
        {"item": "Stapler", "stock": "12", "threshold": "10"}
    ]
    restock = inventory_tracker.get_restock_items(inventory)
    assert len(restock) == 1
    assert restock[0]["item"] == "Printer Paper"
