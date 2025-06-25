"""
Marketing Email Generator using OpenAI
- Generates subject, plain text, and HTML email body
- Inputs: business_type, offer_description, tone
- Saves .txt and .html files
"""
import openai
from typing import Tuple
from utils.config import OPENAI_API_KEY
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

def generate_email(business_type: str, offer_description: str, tone: str) -> Tuple[str, str, str]:
    """Generate subject, plain text, and HTML email using OpenAI."""
    prompt = (
        f"Business type: {business_type}\n"
        f"Offer: {offer_description}\n"
        f"Tone: {tone}"
    )
    messages = [
        {"role": "system", "content": EMAIL_PROMPT},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500
    )
    import json
    result = json.loads(response.choices[0].message.content)
    return result["subject"], result["plain"], result["html"]

def save_email_files(subject: str, plain: str, html: str, out_dir: str = "generated_emails") -> None:
    """Save subject, plain, and HTML email to files."""
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, subject.replace(" ", "_").replace("/", "-")[:50])
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n\n{plain}")
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(f"<h2>{subject}</h2>\n{html}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Marketing Email Generator")
    parser.add_argument("--business_type", required=True, type=str, help="Type of business")
    parser.add_argument("--offer_description", required=True, type=str, help="Offer description")
    parser.add_argument("--tone", required=True, type=str, help="Email tone (e.g., friendly, formal)")
    parser.add_argument("--out_dir", type=str, default="generated_emails", help="Output directory")
    args = parser.parse_args()

    subject, plain, html = generate_email(args.business_type, args.offer_description, args.tone)
    print(f"Subject: {subject}\n\nPlain Text:\n{plain}\n\nHTML:\n{html}")
    save_email_files(subject, plain, html, args.out_dir)
    print(f"Saved to {args.out_dir}")

if __name__ == "__main__":
    main()
