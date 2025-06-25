"""
FAQ Chatbot for Small Business Customer Service
- CLI chatbot loop
- Minimal Flask API endpoint
"""
import openai
from flask import Flask, request, jsonify
from typing import List, Dict
from utils.config import OPENAI_API_KEY
import csv

openai.api_key = OPENAI_API_KEY

def load_csv_data(filepath: str) -> list:
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

LOCATIONS = load_csv_data('data/sample_locations.csv')
PROMOTIONS = load_csv_data('data/sample_promotions.csv')
HOLIDAYS = load_csv_data('data/sample_holidays.csv')
TESTIMONIALS = load_csv_data('data/sample_testimonials.csv')

FAQS: List[Dict[str, str]] = [
    {"question": "What are your business hours?", "answer": "We are open Monday to Friday, 9am to 6pm. See our locations for specific hours."},
    {"question": "Where are you located?", "answer": "We have multiple locations. See below for details."},
    {"question": "How can I contact support?", "answer": "Email support@business.com or call (555) 123-4567. For specific locations, see below."},
    {"question": "Do you offer discounts?", "answer": "Yes! See our current promotions below."},
    {"question": "Are you open on holidays?", "answer": "Holiday hours may vary. See below for details."},
    {"question": "What is your return policy?", "answer": "Returns are accepted within 30 days with receipt."},
    {"question": "How do I book an appointment?", "answer": "You can book online, by phone, or in person at any location."},
    {"question": "What payment methods do you accept?", "answer": "We accept Visa, MasterCard, PayPal, and Apple Pay."},
    {"question": "Do you have customer testimonials?", "answer": "Yes! See below for what our customers say."},
    {"question": "What promotions are running?", "answer": "See our current promotions below."}
]

SYSTEM_PROMPT = "You are a helpful small business FAQ assistant. Answer only based on the provided FAQs."


def get_faq_context() -> str:
    """Format FAQs for LLM context."""
    return "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in FAQS])


def get_extra_context() -> str:
    context = []
    if LOCATIONS:
        context.append("Locations:\n" + "\n".join([f"- {l['location']}: {l['address']} ({l['phone']}), Hours: {l['hours']}" for l in LOCATIONS]))
    if PROMOTIONS:
        context.append("Promotions:\n" + "\n".join([f"- {p['promotion']}: {p['description']} (valid until {p['valid_until']})" for p in PROMOTIONS]))
    if HOLIDAYS:
        context.append("Holiday Hours:\n" + "\n".join([f"- {h['holiday']} ({h['date']}): {'Open ' + h['special_hours'] if h['is_open']=='Yes' else 'Closed'}" for h in HOLIDAYS]))
    if TESTIMONIALS:
        context.append("Testimonials:\n" + "\n".join([f"- {t['customer']}: '{t['quote']}' (Rating: {t['rating']}/5)" for t in TESTIMONIALS]))
    return "\n\n".join(context)


def ask_faq_bot(user_question: str) -> str:
    """Query OpenAI with FAQ and extra context and user question."""
    context = get_faq_context() + "\n\n" + get_extra_context()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + context},
        {"role": "user", "content": user_question}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't process your request: {e}"


def cli_chatbot_loop():
    print("Welcome to the Small Business FAQ Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        answer = ask_faq_bot(user_input)
        print(f"Bot: {answer}")

# Minimal Flask API
app = Flask(__name__)

@app.route("/faq", methods=["POST"])
def faq_api():
    data = request.get_json()
    question = data.get("question", "")
    answer = ask_faq_bot(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Small Business FAQ Chatbot")
    parser.add_argument("--cli", action="store_true", help="Run CLI chatbot loop")
    parser.add_argument("--api", action="store_true", help="Run Flask API server")
    args = parser.parse_args()
    if args.cli:
        cli_chatbot_loop()
    elif args.api:
        app.run(host="0.0.0.0", port=5000)
    else:
        print("Specify --cli for CLI or --api for API mode.")
