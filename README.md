# 📊 Nexus Corporate Valuation Engine

A real-time **Discounted Cash Flow (DCF)** valuation application built with Python and Streamlit. Enter any US stock ticker to instantly calculate intrinsic value using live financial data from Yahoo Finance.

## Features

- **Live Data Integration** — Pulls real-time financials (Revenue, EBITDA, FCF, Beta, etc.) via `yfinance`
- **WACC Calculator** — Computes the Weighted Average Cost of Capital using the Capital Asset Pricing Model (CAPM)
- **DCF Engine** — Projects Free Cash Flow forward, calculates Terminal Value (Gordon Growth Model), and discounts to present value
- **Three Key Outputs** — Enterprise Value, Equity Value, and Per-Share Intrinsic Value
- **Interactive Sliders** — Adjust Risk-Free Rate, Equity Risk Premium, Growth Rates, and Projection Period in real time
- **Sensitivity Analysis Heatmap** — Visualizes how Per-Share Value changes across WACC and Terminal Growth Rate scenarios
- **Buy / Hold / Sell Verdict** — Automatically compares intrinsic value to market price

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend & UI | Streamlit |
| Financial Data | yfinance (Yahoo Finance) |
| Visualizations | Plotly |
| Calculations | NumPy, Pandas |

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/corporate-valuation-dcf.git
cd corporate-valuation-dcf

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## How It Works

1. **Enter a ticker** (e.g., AAPL, NVDA, MSFT)
2. **Adjust assumptions** using the sidebar sliders (WACC components, growth rates)
3. **View results** — Enterprise Value, Equity Value, and Per-Share Intrinsic Value update instantly
4. **Analyze sensitivity** — The heatmap shows how valuation changes with different WACC and terminal growth assumptions

## Course

Built for **MGMT 490AIFA — AI Finance Application** (Spring 2026)

## License

This project is for educational purposes only. Not financial advice.
