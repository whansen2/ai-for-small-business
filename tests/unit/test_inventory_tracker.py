"""
Test for automation/inventory_tracker.py
"""
import pytest
from automation import inventory_tracker

def test_get_restock_items():
    inventory = [
        {"item": "A", "stock": "2", "threshold": "5"},
        {"item": "B", "stock": "10", "threshold": "8"}
    ]
    restock = inventory_tracker.get_restock_items(inventory)
    assert isinstance(restock, list)
    assert any(item["item"] == "A" for item in restock)
    assert all(int(item["stock"]) < int(item["threshold"]) for item in restock)
