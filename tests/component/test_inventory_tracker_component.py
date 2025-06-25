"""
Component tests for automation/inventory_tracker.py
Covers normal, no restock, and malformed inventory scenarios.
"""
import os
import pytest
from automation import inventory_tracker

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

def test_inventory_tracker_real_openai():
    inventory = [
        {"item": "Printer Paper", "stock": "2", "threshold": "10"},
        {"item": "HP 61 Black Ink Cartridge", "stock": "1", "threshold": "5"}
    ]
    restock = inventory_tracker.get_restock_items(inventory)
    summary = inventory_tracker.generate_restock_summary(restock)
    assert "summary" in summary
    assert "email" in summary
    assert len(summary["summary"]) > 0
    assert len(summary["email"]) > 0

def test_inventory_tracker_no_restock():
    inventory = [
        {"item": "A", "stock": "10", "threshold": "5"}
    ]
    restock = inventory_tracker.get_restock_items(inventory)
    assert restock == []

def test_inventory_tracker_malformed():
    inventory = [
        {"item": "B", "stock": "notanumber", "threshold": "5"}
    ]
    restock = inventory_tracker.get_restock_items(inventory)
    assert restock == []
