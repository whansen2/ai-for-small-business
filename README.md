# AI for Small Business

A robust, production-grade Python AI toolkit for small business owners. Focused on practical, real-world automation and intelligence—save time, reduce overhead, and boost decision-making without complexity.

## Features
- **Customer Service**: FAQ chatbot (CLI & API), sentiment analysis for emails/reviews (OpenAI-powered, robust error handling)
- **Marketing**: Automated marketing email generator (plain & HTML, with promotions, robust to malformed responses)
- **Analytics**: Sales forecasting (Prophet, ARIMA, Linear Regression), KPI dashboard (Streamlit, PDF export, advanced metrics)
- **Operations**: Invoice OCR & extraction (robust, preserves original formatting), appointment scheduler (with .ics export, flexible slot logic)
- **Automation**: Monthly PDF business reports (with sales, sentiment, testimonials), inventory tracker (restock summary, email draft)
- **Utils**: Helpers for CSV, JSON, PDF, and secure config loading
- **Comprehensive sample data**: Realistic, safe, and fictitious CSVs for all modules
- **Comprehensive test suite**: Pytest-based, with OpenAI call mocking, robust edge/cross-module/component tests
- **Security**: API key loaded securely from `.env` (never hardcoded)
- **Error Handling**: All OpenAI and file operations have robust error handling and debug logging

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
- **Error Handling:** All modules include robust error handling and debug output for OpenAI and file operations.

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
- **Component and cross-module tests**: Real OpenAI API key required for integration tests. Tests skip gracefully if API/network is unavailable.
- **Edge case coverage**: All modules and tests cover normal, edge, and error scenarios.

## Contributing
Pull requests welcome! Focus on practical, simple solutions that serve small business needs. All code must be modular, PEP8-compliant, and include robust error handling and tests.

## License
MIT License
