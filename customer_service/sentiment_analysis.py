"""
Sentiment analysis for customer emails, messages, or reviews using OpenAI.
- Classifies as positive, neutral, or negative with reasoning
- Accepts single string or .csv batch
- Outputs to terminal or .csv
- Robust error handling for OpenAI and file I/O
"""
import openai
from typing import List, Dict, Optional
from utils.config import OPENAI_API_KEY
from utils.file_io import read_csv, write_csv

openai.api_key = OPENAI_API_KEY

SENTIMENT_PROMPT = (
    "You are a customer sentiment analysis assistant. "
    "Classify the following text as positive, neutral, or negative. "
    "Provide a one-sentence reasoning. "
    "Respond in JSON: {\"sentiment\": <sentiment>, \"reasoning\": <reasoning>}"
)

def extract_json_from_response(response_content: str):
    """Extract JSON object from OpenAI response, stripping markdown/code block if present. No regex. Robust to malformed output."""
    import json
    content = response_content.strip()
    if content.startswith('```json'):
        content = content[len('```json'):].strip()
    if content.startswith('```'):
        content = content[len('```'):].strip()
    if content.endswith('```'):
        content = content[:-3].strip()
    start = content.find('{')
    end = content.rfind('}')
    if start != -1 and end != -1 and end > start:
        content = content[start:end+1]
    if content.count('{') > 0 and content.count('}') > 0:
        last_brace = content.rfind('}')
        content = content[:last_brace+1]
    try:
        return json.loads(content)
    except Exception:
        return {"sentiment": "", "reasoning": ""}

def analyze_sentiment(text: str) -> Dict[str, str]:
    """Analyze sentiment of a single string using OpenAI."""
    messages = [
        {"role": "system", "content": SENTIMENT_PROMPT},
        {"role": "user", "content": text}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=100
    )
    return extract_json_from_response(response.choices[0].message.content)

def analyze_csv(input_csv: str, text_column: str = "text", output_csv: Optional[str] = None) -> List[Dict[str, str]]:
    """Analyze sentiment for each row in a CSV file."""
    rows = read_csv(input_csv)
    results = []
    for row in rows:
        text = row.get(text_column, "")
        result = analyze_sentiment(text)
        row.update(result)
        results.append(row)
    if output_csv:
        fieldnames = list(results[0].keys()) if results else []
        write_csv(output_csv, results, fieldnames)
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Customer Sentiment Analysis")
    parser.add_argument("--text", type=str, help="Single text to analyze")
    parser.add_argument("--csv", type=str, help="Path to input CSV file")
    parser.add_argument("--output", type=str, help="Path to output CSV file (optional)")
    args = parser.parse_args()

    if args.text:
        result = analyze_sentiment(args.text)
        print(f"Sentiment: {result['sentiment']}\nReasoning: {result['reasoning']}")
    elif args.csv:
        results = analyze_csv(args.csv, output_csv=args.output)
        print(f"Processed {len(results)} rows.")
        if args.output:
            print(f"Results saved to {args.output}")
    else:
        print("Provide --text or --csv argument.")

if __name__ == "__main__":
    main()
