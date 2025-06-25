"""
Unit tests for finance/expense_tracker.py
"""
import os
import pytest
from finance.expense_tracker import ExpenseTracker

SAMPLE_CSV = os.path.join(os.path.dirname(__file__), '../../data/sample_bank.csv')

def test_read_csv():
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    assert isinstance(txs, list)
    assert len(txs) > 0
    assert all('Date' in tx and 'Description' in tx and 'Amount' in tx for tx in txs)

def test_monthly_cash_flow():
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    summary = tracker.monthly_cash_flow(txs)
    assert isinstance(summary, dict)
    assert '2025-06' in summary
    assert 'inflow' in summary['2025-06'] and 'outflow' in summary['2025-06']

def test_detect_anomalies():
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    anomalies = tracker.detect_anomalies(txs, threshold=1000)
    assert isinstance(anomalies, list)
    assert any(abs(float(tx['Amount'])) >= 1000 for tx in anomalies)

def test_export_to_quickbooks_csv(tmp_path):
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    out = tmp_path / "export_qb.csv"
    tracker.export_to_quickbooks_csv(txs, str(out))
    assert out.exists()
    with open(out) as f:
        lines = f.readlines()
    assert lines[0].startswith('Date,Description,Amount,Category')
