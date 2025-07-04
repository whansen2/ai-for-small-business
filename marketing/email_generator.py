"""
Marketing Email Generator using OpenAI
- Generates subject, plain text, and HTML email body
- Inputs: business_type, offer_description, tone
- Saves .txt and .html files
- Robust error handling and debug logging for OpenAI API calls
"""
import openai
from typing import Tuple
from utils.config import OPENAI_API_KEY
import csv
import os

openai.api_key = OPENAI_API_KEY

EMAIL_PROMPT = (
    "You are a marketing email assistant. "
    "Given a business type, offer description, and tone, generate: "
    "1. A catchy subject line. "
    "2. A plain text email body. "
    "3. An HTML email body. "
    "Respond in JSON: {\"subject\": <subject>, \"plain\": <plain>, \"html\": <html>}"
)

def extract_json_from_response(response_content: str):
    """Extract JSON object from OpenAI response, stripping markdown/code block if present. No regex. Robust to malformed output."""
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
    # Defensive: truncate at last closing brace if extra text follows
    if content.count('{') > 0 and content.count('}') > 0:
        last_brace = content.rfind('}')
        content = content[:last_brace+1]
    try:
        return json.loads(content)
    except Exception:
        # Fallback: return minimal valid structure
        return {"subject": "", "plain": "", "html": ""}

def generate_email(business_type: str, offer_description: str, tone: str) -> Tuple[str, str, str]:
    """Generate subject, plain text, and HTML email using OpenAI. Logs errors and raw responses for debugging."""
    prompt = (
        f"Business type: {business_type}\n"
        f"Offer: {offer_description}\n"
        f"Tone: {tone}"
    )
    messages = [
        {"role": "system", "content": EMAIL_PROMPT},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500
        )
        raw_content = response.choices[0].message.content
        print("[DEBUG] OpenAI raw response:", raw_content)
        result = extract_json_from_response(raw_content)
        if not result["subject"] or not result["plain"] or not result["html"]:
            print("[ERROR] OpenAI response missing expected fields:", result)
        return result["subject"], result["plain"], result["html"]
    except Exception as e:
        print(f"[ERROR] OpenAI API call failed: {e}")
        return (f"[ERROR] {e}", f"[ERROR] {e}", f"[ERROR] {e}")

def save_email_files(subject: str, plain: str, html: str, out_dir: str = "generated_emails") -> None:
    """Save subject, plain, and HTML email to files."""
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, subject.replace(" ", "_").replace("/", "-")[:50])
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n\n{plain}")
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(f"<h2>{subject}</h2>\n{html}")

def load_promotions(filepath: str = "data/sample_promotions.csv") -> list:
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Marketing Email Generator")
    parser.add_argument("--business_type", required=True, type=str, help="Type of business")
    parser.add_argument("--offer_description", type=str, help="Offer description")
    parser.add_argument("--tone", required=True, type=str, help="Email tone (e.g., friendly, formal)")
    parser.add_argument("--promotion", action="store_true", help="Use a current promotion from sample_promotions.csv")
    parser.add_argument("--out_dir", type=str, default="generated_emails", help="Output directory")
    args = parser.parse_args()

    offer_description = args.offer_description
    if args.promotion:
        promotions = load_promotions()
        if promotions:
            promo = promotions[0]  # Use the first valid promotion
            offer_description = f"{promo['promotion']}: {promo['description']} (Valid until {promo['valid_until']})"
            print(f"Using promotion: {offer_description}")
        else:
            print("No promotions found. Please provide --offer_description.")
            return
    elif not offer_description:
        print("You must provide --offer_description or use --promotion.")
        return

    subject, plain, html = generate_email(args.business_type, offer_description, args.tone)
    print(f"Subject: {subject}\n\nPlain Text:\n{plain}\n\nHTML:\n{html}")
    save_email_files(subject, plain, html, args.out_dir)
    print(f"Saved to {args.out_dir}")

if __name__ == "__main__":
    main()
