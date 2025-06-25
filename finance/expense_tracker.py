"""
AI-powered Expense Tracker for Small Businesses
- Reads CSV or PDF bank/credit card transactions
- Categorizes expenses using OpenAI
- Produces monthly cash flow summaries and highlights anomalies
- Can export to QuickBooks/Xero CSV formats
"""
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

try:
    import openai
except ImportError:
    openai = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

class ExpenseTracker:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if openai and self.openai_api_key:
            openai.api_key = self.openai_api_key

    def read_csv(self, filepath: str) -> List[Dict]:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def read_pdf(self, filepath: str) -> List[str]:
        if not pdfplumber:
            raise ImportError("pdfplumber is required for PDF extraction.")
        with pdfplumber.open(filepath) as pdf:
            text = []
            for page in pdf.pages:
                text.append(page.extract_text())
            return text

    def categorize_expenses(self, transactions: List[Dict]) -> List[Dict]:
        if not openai:
            raise ImportError("openai is required for AI categorization.")
        for tx in transactions:
            description = tx.get('Description') or tx.get('details') or ''
            prompt = f"Categorize this expense: '{description}'. Categories: Office, Marketing, Supplies, Travel, Meals, Utilities, Rent, Payroll, Taxes, Other. Respond with only the category."
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10,
                )
                category = response.choices[0].message.content.strip()
                tx['Category'] = category
            except Exception as e:
                tx['Category'] = 'Uncategorized'
                tx['AI_Error'] = str(e)
        return transactions

    def monthly_cash_flow(self, transactions: List[Dict], date_field: str = 'Date', amount_field: str = 'Amount') -> Dict[str, Dict[str, float]]:
        summary = {}
        for tx in transactions:
            date_str = tx.get(date_field)
            amount = float(tx.get(amount_field, 0))
            try:
                month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
            except Exception:
                month = 'Unknown'
            if month not in summary:
                summary[month] = {'inflow': 0.0, 'outflow': 0.0}
            if amount >= 0:
                summary[month]['inflow'] += amount
            else:
                summary[month]['outflow'] += amount
        return summary

    def detect_anomalies(self, transactions: List[Dict], threshold: float = 1000.0) -> List[Dict]:
        anomalies = []
        for tx in transactions:
            try:
                amount = abs(float(tx.get('Amount', 0)))
                if amount >= threshold:
                    anomalies.append(tx)
            except Exception:
                continue
        return anomalies

    def export_to_quickbooks_csv(self, transactions: List[Dict], filepath: str):
        fields = ['Date', 'Description', 'Amount', 'Category']
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for tx in transactions:
                writer.writerow({k: tx.get(k, '') for k in fields})
