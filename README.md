# AI for Small Business

A collection of Python-based AI tools designed for small business owners. These tools focus on practical, "mom and pop" use cases—automation and intelligence that save time, reduce overhead, and boost decision-making without complexity.

## Features
- **Customer Service**: FAQ chatbot (CLI & API), sentiment analysis for emails/reviews
- **Marketing**: Automated marketing email generator (plain & HTML, with promotions)
- **Analytics**: Sales forecasting (Prophet, ARIMA, Linear Regression), KPI dashboard (Streamlit, PDF export, advanced metrics)
- **Operations**: Invoice OCR & extraction (robust, preserves original formatting), appointment scheduler (with .ics export)
- **Automation**: Monthly PDF business reports (with sales, sentiment, testimonials), inventory tracker (restock summary, email draft)
- **Utils**: Helpers for CSV, JSON, PDF, and secure config loading
- **Comprehensive sample data**: Realistic, safe, and fictitious CSVs for all modules
- **Comprehensive test suite**: Pytest-based, with OpenAI call mocking

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/ai-for-small-business.git
   cd ai-for-small-business
   ```
2. **Set up your environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure your OpenAI API key:**
   - Copy `.env.example` to `.env`:
     ```sh
     cp .env.example .env
     ```
   - Edit `.env` and add your real OpenAI API key:
     ```env
     OPENAI_API_KEY=sk-...
     ```
   - **Your API key is loaded securely via `utils/config.py` using `python-dotenv`. Never hardcode secrets!**

4. **Run a tool (example):**
   ```sh
   python3 marketing/email_generator.py --business_type "Retail Store" --offer_description "20% off all cleaning services" --tone friendly
   ```

## Security & Best Practices
- **API Key Safety:** Your OpenAI API key is never hardcoded. It is loaded from `.env` using `python-dotenv` in `utils/config.py` and imported wherever needed.
- **Model:** All LLM tasks use OpenAI's `gpt-4o` for best results.
- **Sample Data:** All provided data is fictitious but realistic—safe for demos and testing.

## Project Structure
```
ai-for-small-business/
├── customer_service/         # Chatbot, sentiment analysis
├── marketing/                # Email generator
├── analytics/                # Sales forecast, KPI dashboard
├── operations/               # Invoice processor, appointment scheduler
├── automation/               # Report generator, inventory tracker
├── utils/                    # file_io.py, config.py
├── data/                     # Realistic sample CSVs
├── tests/                    # Pytest suite for all modules
├── .env.example              # Example env file
├── requirements.txt          # All dependencies
├── README.md                 # This file
└── LICENSE
```

## Testing
- Run all tests with:
  ```sh
  pytest
  ```
- All major modules are covered, with OpenAI calls mocked for reliability.

## Contributing
Pull requests welcome! Focus on practical, simple solutions that serve small business needs.

## License
MIT License
