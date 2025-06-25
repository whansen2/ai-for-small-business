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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        file_io.write_csv(tmp.name, data, fieldnames)
        read = file_io.read_csv(tmp.name)
        assert read == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
    os.remove(tmp.name)
