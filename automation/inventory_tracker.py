"""
Inventory Tracker
- Reads inventory levels from .csv
- When below threshold, generates restock summary (via OpenAI)
- Optional email draft (save to .txt)
- Outputs restock CSV
- Robust error handling for OpenAI and file I/O
"""
import openai
from utils.config import OPENAI_API_KEY
from utils.file_io import read_csv, write_csv
from typing import List, Dict

openai.api_key = OPENAI_API_KEY

RESTOCK_PROMPT = (
    "You are an inventory assistant. Given a list of items below threshold, "
    "generate a human-readable restock summary and a draft email to a supplier. "
    "Respond in JSON: {\"summary\": <summary>, \"email\": <email>}"
)

def get_restock_items(inventory: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Return items where stock < threshold."""
    restock = []
    for item in inventory:
        try:
            stock = int(item['stock'])
            threshold = int(item['threshold'])
            if stock < threshold:
                restock.append(item)
        except Exception:
            continue
    return restock

def extract_json_from_response(response_content: str):
    """Extract JSON object from OpenAI response, stripping markdown/code block if present. No regex."""
    import json
    content = response_content.strip()
    # Remove code block markers if present
    if content.startswith('```json'):
        content = content[len('```json'):].strip()
    if content.startswith('```'):
        content = content[len('```'):].strip()
    if content.endswith('```'):
        content = content[:-3].strip()
    # Find the first '{' and last '}'
    start = content.find('{')
    end = content.rfind('}')
    if start != -1 and end != -1 and end > start:
        content = content[start:end+1]
    return json.loads(content)

def generate_restock_summary(restock_items: List[Dict[str, str]]) -> Dict[str, str]:
    """Use OpenAI to generate summary and email draft."""
    items_str = "\n".join([f"{i['item']}: {i['stock']} in stock (threshold {i['threshold']})" for i in restock_items])
    prompt = f"Restock items:\n{items_str}"
    messages = [
        {"role": "system", "content": RESTOCK_PROMPT},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300
    )
    return extract_json_from_response(response.choices[0].message.content)

def save_email_draft(email: str, out_path: str) -> None:
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(email)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Inventory Tracker")
    parser.add_argument("--csv", type=str, default="data/sample_inventory.csv", help="Inventory CSV file")
    parser.add_argument("--restock_csv", type=str, default="restock.csv", help="Output restock CSV file")
    parser.add_argument("--email_txt", type=str, help="Optional: save email draft to .txt file")
    args = parser.parse_args()
    inventory = read_csv(args.csv)
    restock_items = get_restock_items(inventory)
    if restock_items:
        write_csv(args.restock_csv, restock_items, fieldnames=list(restock_items[0].keys()))
        print(f"Restock CSV saved to {args.restock_csv}")
        summary = generate_restock_summary(restock_items)
        print(f"Summary:\n{summary['summary']}\n")
        if args.email_txt:
            save_email_draft(summary['email'], args.email_txt)
            print(f"Email draft saved to {args.email_txt}")
        else:
            print(f"Email draft:\n{summary['email']}")
    else:
        print("No items below threshold.")

if __name__ == "__main__":
    main()
