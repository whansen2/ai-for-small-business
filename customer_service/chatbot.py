"""
FAQ Chatbot for Small Business Customer Service
- CLI chatbot loop
- Minimal Flask API endpoint
"""
import openai
from flask import Flask, request, jsonify
from typing import List, Dict
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

FAQS: List[Dict[str, str]] = [
    {"question": "What are your business hours?", "answer": "We are open Monday to Friday, 9am to 6pm."},
    {"question": "Where are you located?", "answer": "123 Main Street, Hometown, USA."},
    {"question": "What is your return policy?", "answer": "Returns are accepted within 30 days with receipt."},
    {"question": "How can I contact support?", "answer": "Email support@business.com or call (555) 123-4567."},
    {"question": "Do you offer discounts?", "answer": "We offer seasonal promotions and discounts for loyal customers."},
    {"question": "How do I track my order?", "answer": "Log in to your account and view order status under 'My Orders'."},
    {"question": "Are your products eco-friendly?", "answer": "Yes, we prioritize sustainable and eco-friendly products."},
    {"question": "Can I change my order after placing it?", "answer": "Contact us within 2 hours to request changes."},
    {"question": "Do you offer gift wrapping?", "answer": "Yes, gift wrapping is available at checkout for a small fee."},
    {"question": "What payment methods do you accept?", "answer": "We accept Visa, MasterCard, PayPal, and Apple Pay."}
]

SYSTEM_PROMPT = "You are a helpful small business FAQ assistant. Answer only based on the provided FAQs."


def get_faq_context() -> str:
    """Format FAQs for LLM context."""
    return "\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in FAQS])


def ask_faq_bot(user_question: str) -> str:
    """Query OpenAI with FAQ context and user question."""
    context = get_faq_context()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + context},
        {"role": "user", "content": user_question}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()


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
