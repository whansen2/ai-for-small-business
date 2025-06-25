"""
Component tests for finance/expense_tracker.py
Covers AI categorization and end-to-end workflow with real OpenAI API key.
"""
import os
import pytest
from finance.expense_tracker import ExpenseTracker

pytestmark = pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key set.")

SAMPLE_CSV = os.path.join(os.path.dirname(__file__), '../../data/sample_bank.csv')

def test_categorize_expenses_real_openai():
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    txs = tracker.categorize_expenses(txs)
    assert isinstance(txs, list)
    assert all('Category' in tx for tx in txs)
    # At least one transaction should be categorized as something other than Uncategorized
    assert any(tx['Category'] != 'Uncategorized' for tx in txs)

def test_end_to_end_workflow():
    tracker = ExpenseTracker()
    txs = tracker.read_csv(SAMPLE_CSV)
    txs = tracker.categorize_expenses(txs)
    summary = tracker.monthly_cash_flow(txs)
    anomalies = tracker.detect_anomalies(txs, threshold=1000)
    assert isinstance(summary, dict)
    assert isinstance(anomalies, list)
    # Export and check file
    out = os.path.join(os.path.dirname(__file__), '../../data/export_qb_component.csv')
    tracker.export_to_quickbooks_csv(txs, out)
    assert os.path.exists(out)
    with open(out) as f:
        lines = f.readlines()
    assert lines[0].startswith('Date,Description,Amount,Category')
