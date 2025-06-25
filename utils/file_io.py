"""
Helper functions for reading and writing CSV, JSON, and PDF files.
- Robust to malformed files and encoding issues
"""
import csv
import json
from typing import Any, List, Dict


def read_csv(filepath: str) -> List[Dict[str, Any]]:
    """Read a CSV file and return a list of dictionaries."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(filepath: str, data: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    """Write a list of dictionaries to a CSV file."""
    with open(filepath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_json(filepath: str) -> Any:
    """Read a JSON file and return the data."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        return json.load(f)


def write_json(filepath: str, data: Any) -> None:
    """Write data to a JSON file."""
    with open(filepath, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
