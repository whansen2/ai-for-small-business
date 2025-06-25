"""
Minimal OpenAI GPT-4o connectivity and key test.
Run this script to verify your API key, network, and model access.
"""
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("[SUCCESS] OpenAI GPT-4o response:")
    print(response)
except Exception as e:
    print("[ERROR] OpenAI API call failed:", e)
    print("Check your API key, network, and model access.")
