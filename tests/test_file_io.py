"""
Test for utils/file_io.py
"""
import pytest
from utils import file_io
import tempfile
import os

def test_csv_io():
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    fieldnames = ["a", "b"]
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', newline='') as f:
        file_io.write_csv(f.name, data, fieldnames)
        f.seek(0)
        rows = file_io.read_csv(f.name)
    assert rows == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
    os.remove(f.name)
