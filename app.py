"""
╔═══════════════════════════════════════════════════════════════════════╗
║              NEXUS CORPORATE VALUATION ENGINE                       ║
║              DCF-Based Intrinsic Value Calculator                   ║
║              MGMT 490 AI Finance Application                        ║
╚═══════════════════════════════════════════════════════════════════════╝

This application performs a Discounted Cash Flow (DCF) valuation using
real financial data from Yahoo Finance. Users can adjust key assumptions
(WACC, Growth Rates) and instantly see the impact on intrinsic value.

Author: Max Clark
Course: MGMT 490AIFA — Spring 2026
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG & CUSTOM THEME
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus Valuation Engine | DCF Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject premium dark theme CSS
st.markdown("""
<style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0e1a;
        --bg-card: rgba(15, 23, 42, 0.85);
        --bg-card-hover: rgba(20, 30, 55, 0.9);
        --border-color: rgba(99, 102, 241, 0.15);
        --border-glow: rgba(99, 102, 241, 0.4);
        --primary: #6366f1;
        --primary-light: #818cf8;
        --secondary: #a855f7;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    /* ── Global ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 40%, #1a1040 100%);
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #160f30 100%);
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] span,
    section[data-testid="stSidebar"] .stElementContainer label {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] caption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    /* ── Metric Cards ── */
    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px 24px;
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: var(--border-glow);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.75rem !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* ── Custom metric cards ── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
        transform: translateY(-3px);
    }
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .metric-value.green {
        background: linear-gradient(135deg, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-value.blue {
        background: linear-gradient(135deg, #06b6d4, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-value.gold {
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-sub {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 4px;
    }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-color);
    }
    .section-header h2 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .section-icon {
        font-size: 1.5rem;
    }

    /* ── Glass panel ── */
    .glass-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }

    /* ── Data Table ── */
    .dataframe {
        background: transparent !important;
        color: var(--text-primary) !important;
    }

    /* ── Hero Title ── */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin-bottom: 8px;
    }
    .hero-gradient {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 24px;
    }

    /* ── Ticker badge ── */
    .ticker-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        padding: 8px 24px;
        border-radius: 12px;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        margin-bottom: 8px;
    }
    .company-name {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* ── Verdict Badge ── */
    .verdict-buy {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }
    .verdict-hold {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }
    .verdict-sell {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }

    /* ── Expander ── */
    details {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }

    /* ── Hide default streamlit elements ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Sensitivity table ── */
    .sensitivity-cell-green { color: #10b981; font-weight: 700; }
    .sensitivity-cell-red { color: #ef4444; font-weight: 700; }
    .sensitivity-cell-gold { color: #fbbf24; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def format_large_number(num):
    """Format large numbers into human-readable strings (e.g., $1.5T, $200B)."""
    if num is None or np.isnan(num):
        return "N/A"
    abs_num = abs(num)
    sign = "-" if num < 0 else ""
    if abs_num >= 1e12:
        return f"{sign}${abs_num / 1e12:.2f}T"
    elif abs_num >= 1e9:
        return f"{sign}${abs_num / 1e9:.2f}B"
    elif abs_num >= 1e6:
        return f"{sign}${abs_num / 1e6:.1f}M"
    else:
        return f"{sign}${abs_num:,.0f}"


def format_currency(num):
    """Format a number as currency with 2 decimal places."""
    if num is None or np.isnan(num):
        return "N/A"
    return f"${num:,.2f}"


@st.cache_data(ttl=60, show_spinner=False)
def fetch_financial_data(ticker_symbol, _refresh_key=None):
    """
    Fetch comprehensive financial data from Yahoo Finance.
    Returns a dict with all data needed for the DCF model.
    Cached for 60 seconds. Pass a new _refresh_key to force a fresh pull.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        # Validate that we got real data
        if not info or info.get('regularMarketPrice') is None:
            # Try to get price from history
            hist = stock.history(period="5d")
            if hist.empty:
                return None

        # ── Basic Company Info ──
        company_name = info.get('longName') or info.get('shortName') or ticker_symbol
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if current_price is None:
            hist = stock.history(period="5d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
            else:
                return None

        shares_outstanding = info.get('sharesOutstanding', 0)
        market_cap = info.get('marketCap', current_price * shares_outstanding if shares_outstanding else 0)

        # ── Balance Sheet Data ──
        total_debt = info.get('totalDebt', 0) or 0
        total_cash = info.get('totalCash', 0) or 0

        # ── Cash Flow Data ──
        operating_cf = info.get('operatingCashflow', 0) or 0
        capex = abs(info.get('capitalExpenditures', 0) or 0)
        fcf = info.get('freeCashflow') or (operating_cf - capex)

        # ── Income Statement Data ──
        revenue = info.get('totalRevenue', 0) or 0
        ebitda = info.get('ebitda', 0) or 0
        net_income = info.get('netIncomeToCommon', 0) or 0

        # ── Valuation Metrics ──
        beta = info.get('beta', 1.0) or 1.0
        pe_ratio = info.get('trailingPE')
        ev_to_ebitda = info.get('enterpriseToEbitda')

        # ── Margins ──
        profit_margin = info.get('profitMargins', 0) or 0
        operating_margin = info.get('operatingMargins', 0) or 0

        # ── Revenue Growth (Historical) ──
        revenue_growth = info.get('revenueGrowth', 0) or 0

        # ── Historical Financials (for charts) ──
        try:
            income_stmt = stock.income_stmt
            cashflow_stmt = stock.cashflow
            balance_sheet = stock.balance_sheet
        except:
            income_stmt = pd.DataFrame()
            cashflow_stmt = pd.DataFrame()
            balance_sheet = pd.DataFrame()

        # Extract historical revenue
        hist_revenue = []
        hist_years = []
        if not income_stmt.empty:
            for col in reversed(income_stmt.columns):
                try:
                    rev = income_stmt.loc['Total Revenue', col] if 'Total Revenue' in income_stmt.index else None
                    if rev is not None and not np.isnan(rev):
                        hist_revenue.append(float(rev))
                        hist_years.append(col.year if hasattr(col, 'year') else str(col))
                except:
                    pass

        # Extract historical FCF
        hist_fcf = []
        if not cashflow_stmt.empty:
            for col in reversed(cashflow_stmt.columns):
                try:
                    ocf = cashflow_stmt.loc['Operating Cash Flow', col] if 'Operating Cash Flow' in cashflow_stmt.index else 0
                    cx = cashflow_stmt.loc['Capital Expenditure', col] if 'Capital Expenditure' in cashflow_stmt.index else 0
                    if ocf is not None and not np.isnan(ocf):
                        calculated_fcf = float(ocf) + float(cx)  # CapEx is negative in yfinance
                        hist_fcf.append(calculated_fcf)
                except:
                    pass

        return {
            'company_name': company_name,
            'ticker': ticker_symbol.upper(),
            'sector': sector,
            'industry': industry,
            'current_price': current_price,
            'shares_outstanding': shares_outstanding,
            'market_cap': market_cap,
            'total_debt': total_debt,
            'total_cash': total_cash,
            'operating_cf': operating_cf,
            'capex': capex,
            'fcf': fcf,
            'revenue': revenue,
            'ebitda': ebitda,
            'net_income': net_income,
            'beta': beta,
            'pe_ratio': pe_ratio,
            'ev_to_ebitda': ev_to_ebitda,
            'profit_margin': profit_margin,
            'operating_margin': operating_margin,
            'revenue_growth': revenue_growth,
            'hist_revenue': hist_revenue,
            'hist_years': hist_years,
            'hist_fcf': hist_fcf,
        }

    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol}: {str(e)}")
        return None


def calculate_wacc(risk_free_rate, beta, equity_risk_premium, cost_of_debt,
                   tax_rate, debt_weight, equity_weight):
    """
    Calculate Weighted Average Cost of Capital (WACC).

    WACC = (E/V) × Re + (D/V) × Rd × (1 - T)

    Where:
        Re = Risk-Free Rate + Beta × Equity Risk Premium  (CAPM)
        Rd = Cost of Debt
        T  = Corporate Tax Rate
        E/V = Equity weight in capital structure
        D/V = Debt weight in capital structure
    """
    cost_of_equity = risk_free_rate + beta * equity_risk_premium  # CAPM
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
    return wacc, cost_of_equity


def run_dcf_model(fcf_base, wacc, short_term_growth, terminal_growth,
                  projection_years=5, total_debt=0, total_cash=0,
                  shares_outstanding=1):
    """
    Full DCF Model:

    1. Project Free Cash Flows forward using short-term growth rate
    2. Calculate Terminal Value using Gordon Growth Model:
       TV = FCF_n × (1 + g) / (WACC - g)
    3. Discount all future cash flows and Terminal Value back to present
    4. Enterprise Value = Sum of discounted FCFs + discounted Terminal Value
    5. Equity Value = Enterprise Value - Total Debt + Cash
    6. Per-Share Value = Equity Value / Shares Outstanding
    """
    if wacc <= terminal_growth:
        # Prevent division by zero or negative — WACC must exceed terminal growth
        terminal_growth = wacc - 0.01

    # Step 1: Project FCFs
    projected_fcfs = []
    current_fcf = fcf_base
    for year in range(1, projection_years + 1):
        current_fcf *= (1 + short_term_growth)
        projected_fcfs.append(current_fcf)

    # Step 2: Terminal Value (Gordon Growth Model)
    terminal_value = projected_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

    # Step 3: Discount everything back to present value
    discounted_fcfs = []
    for i, fcf in enumerate(projected_fcfs):
        discount_factor = (1 + wacc) ** (i + 1)
        discounted_fcfs.append(fcf / discount_factor)

    discounted_terminal = terminal_value / ((1 + wacc) ** projection_years)

    # Step 4: Enterprise Value
    pv_of_fcfs = sum(discounted_fcfs)
    enterprise_value = pv_of_fcfs + discounted_terminal

    # Step 5: Equity Value
    equity_value = enterprise_value - total_debt + total_cash

    # Step 6: Per-Share Value
    per_share_value = equity_value / shares_outstanding if shares_outstanding > 0 else 0

    return {
        'projected_fcfs': projected_fcfs,
        'discounted_fcfs': discounted_fcfs,
        'terminal_value': terminal_value,
        'discounted_terminal': discounted_terminal,
        'pv_of_fcfs': pv_of_fcfs,
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'per_share_value': per_share_value,
        'projection_years': projection_years
    }


def generate_sensitivity_table(fcf_base, wacc_range, growth_range,
                               short_term_growth, projection_years,
                               total_debt, total_cash, shares_outstanding):
    """
    Generate a 2D sensitivity analysis table.
    X-axis: WACC values
    Y-axis: Terminal Growth Rate values
    Cell values: Per-Share intrinsic value
    """
    results = []
    for tg in growth_range:
        row = []
        for w in wacc_range:
            dcf = run_dcf_model(
                fcf_base=fcf_base,
                wacc=w,
                short_term_growth=short_term_growth,
                terminal_growth=tg,
                projection_years=projection_years,
                total_debt=total_debt,
                total_cash=total_cash,
                shares_outstanding=shares_outstanding
            )
            row.append(round(dcf['per_share_value'], 2))
        results.append(row)

    df = pd.DataFrame(
        results,
        columns=[f"{w*100:.1f}%" for w in wacc_range],
        index=[f"{g*100:.1f}%" for g in growth_range]
    )
    return df


# ─────────────────────────────────────────────────────────────
# SIDEBAR — MODEL INPUTS
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 16px 0 24px;">
        <div style="font-size: 2rem;">📊</div>
        <div style="font-size: 1.4rem; font-weight: 800; letter-spacing: -0.02em;
                    background: linear-gradient(135deg, #818cf8, #c084fc);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            NEXUS DCF ENGINE
        </div>
        <div style="color: #94a3b8; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase;">
            Corporate Valuation Model
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Ticker Input ──
    st.markdown("### 🔍 Company Selection")
    ticker_input = st.text_input(
        "Enter Ticker Symbol",
        value="AAPL",
        placeholder="e.g., AAPL, MSFT, NVDA",
        help="Enter any publicly traded US stock ticker symbol"
    ).upper().strip()

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        analyze_btn = st.button("🚀 Run Valuation", type="primary", use_container_width=True)
    with btn_col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Bump the refresh key to bust the cache
            st.session_state['refresh_key'] = datetime.now().isoformat()
            st.cache_data.clear()
            st.rerun()

    # ── Data freshness indicator ──
    refresh_ts = st.session_state.get('refresh_key', None)
    if refresh_ts:
        try:
            ts = datetime.fromisoformat(refresh_ts)
            st.caption(f"🟢 Data refreshed at {ts.strftime('%I:%M:%S %p')}")
        except:
            st.caption("🟢 Using live data")
    else:
        st.caption("🟢 Using live market data")

    st.markdown("---")

    # ── WACC Components ──
    st.markdown("### 📐 WACC Assumptions")
    st.caption("Capital Asset Pricing Model (CAPM)")

    risk_free_rate = st.slider(
        "Risk-Free Rate (10Y Treasury)",
        min_value=1.0, max_value=8.0, value=4.2, step=0.1,
        format="%.1f%%",
        help="Current yield on the 10-Year US Treasury Bond"
    ) / 100

    equity_risk_premium = st.slider(
        "Equity Risk Premium",
        min_value=3.0, max_value=8.0, value=5.5, step=0.1,
        format="%.1f%%",
        help="Historical average excess return of equities over risk-free rate"
    ) / 100

    cost_of_debt = st.slider(
        "Pre-Tax Cost of Debt",
        min_value=1.0, max_value=12.0, value=4.5, step=0.1,
        format="%.1f%%",
        help="Company's average interest rate on outstanding debt"
    ) / 100

    tax_rate = st.slider(
        "Corporate Tax Rate",
        min_value=10.0, max_value=40.0, value=21.0, step=0.5,
        format="%.1f%%",
        help="Effective corporate tax rate (US federal = 21%)"
    ) / 100

    st.markdown("---")

    # ── Growth Assumptions ──
    st.markdown("### 📈 Growth Assumptions")

    short_term_growth = st.slider(
        "Short-Term FCF Growth Rate",
        min_value=-10.0, max_value=30.0, value=8.0, step=0.5,
        format="%.1f%%",
        help="Expected annual FCF growth rate over the projection period"
    ) / 100

    terminal_growth = st.slider(
        "Terminal Growth Rate",
        min_value=0.5, max_value=5.0, value=2.5, step=0.1,
        format="%.1f%%",
        help="Long-term sustainable growth rate (typically 2-3%, close to GDP growth)"
    ) / 100

    projection_years = st.slider(
        "Projection Period (Years)",
        min_value=3, max_value=10, value=5, step=1,
        help="Number of years to project Free Cash Flow forward"
    )

    st.markdown("---")

    # ── Quick Presets ──
    st.markdown("### ⚡ Quick Tickers")
    preset_cols = st.columns(3)
    presets = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA"]
    for i, preset in enumerate(presets):
        col = preset_cols[i % 3]
        with col:
            if st.button(preset, key=f"preset_{preset}", use_container_width=True):
                st.session_state['run_ticker'] = preset

    st.markdown("---")
    st.caption("Built for MGMT 490AIFA — Spring 2026")


# ─────────────────────────────────────────────────────────────
# MAIN CONTENT AREA
# ─────────────────────────────────────────────────────────────

# Check if a preset was clicked
active_ticker = st.session_state.get('run_ticker', None) or ticker_input
if 'run_ticker' in st.session_state:
    del st.session_state['run_ticker']

# Hero Header
st.markdown("""
<div style="margin-bottom: 32px;">
    <div class="hero-title">
        <span style="color: #f1f5f9;">Corporate </span>
        <span class="hero-gradient">Valuation Engine</span>
    </div>
    <div class="hero-sub">
        Dynamic DCF modeling with real-time financial data — Adjust WACC, growth rates, and projection horizons to stress-test intrinsic value assumptions.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FETCH DATA & RUN MODEL ───
if active_ticker:
    # Use refresh key to bust cache when user clicks "Refresh Data"
    refresh_key = st.session_state.get('refresh_key', 'default')
    with st.spinner(f"Fetching financial data for **{active_ticker}**..."):
        data = fetch_financial_data(active_ticker, _refresh_key=refresh_key)

    if data is None:
        st.error(f"❌ Could not retrieve data for ticker **{active_ticker}**. Please check the symbol and try again.")
        st.info("💡 **Tip:** Make sure you enter a valid US stock ticker (e.g., AAPL, MSFT, NVDA)")
        st.stop()

    # ── Extract data ──
    fcf_base = data['fcf']
    beta = data['beta']
    total_debt = data['total_debt']
    total_cash = data['total_cash']
    shares = data['shares_outstanding']
    current_price = data['current_price']

    # ── Calculate Capital Structure Weights ──
    equity_market_value = data['market_cap']
    total_capital = equity_market_value + total_debt
    equity_weight = equity_market_value / total_capital if total_capital > 0 else 0.8
    debt_weight = total_debt / total_capital if total_capital > 0 else 0.2

    # ── Calculate WACC ──
    wacc, cost_of_equity = calculate_wacc(
        risk_free_rate=risk_free_rate,
        beta=beta,
        equity_risk_premium=equity_risk_premium,
        cost_of_debt=cost_of_debt,
        tax_rate=tax_rate,
        debt_weight=debt_weight,
        equity_weight=equity_weight
    )

    # ── Handle edge case: negative or zero FCF ──
    if fcf_base <= 0:
        st.warning(f"⚠️ **{active_ticker}** has negative or zero Free Cash Flow (${fcf_base:,.0f}). "
                   "The DCF model may produce unreliable results. Consider the company's path to positive FCF.")
        # Use a small positive number to avoid breaking the model
        if fcf_base == 0:
            fcf_base = 1  # Avoid division by zero

    # ── Run DCF Model ──
    dcf_result = run_dcf_model(
        fcf_base=fcf_base,
        wacc=wacc,
        short_term_growth=short_term_growth,
        terminal_growth=terminal_growth,
        projection_years=projection_years,
        total_debt=total_debt,
        total_cash=total_cash,
        shares_outstanding=shares
    )

    # ═══════════════════════════════════════════════════════════
    # SECTION 1: COMPANY HEADER
    # ═══════════════════════════════════════════════════════════

    header_col1, header_col2 = st.columns([2, 3])

    with header_col1:
        st.markdown(f"""
        <div>
            <div class="ticker-badge">{data['ticker']}</div>
            <div class="company-name">{data['company_name']}</div>
            <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px;">
                {data['sector']} · {data['industry']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with header_col2:
        # Determine verdict
        per_share = dcf_result['per_share_value']
        upside = ((per_share - current_price) / current_price) * 100 if current_price > 0 else 0

        if upside > 15:
            verdict_class = "verdict-buy"
            verdict_text = "🟢 UNDERVALUED — BUY"
        elif upside > -10:
            verdict_class = "verdict-hold"
            verdict_text = "🟡 FAIRLY VALUED — HOLD"
        else:
            verdict_class = "verdict-sell"
            verdict_text = "🔴 OVERVALUED — SELL"

        st.markdown(f"""
        <div style="text-align: right;">
            <div style="color: var(--text-secondary); font-size: 0.75rem; text-transform: uppercase;
                        letter-spacing: 0.1em; margin-bottom: 4px;">Current Market Price</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: var(--text-primary);">
                {format_currency(current_price)}
            </div>
            <div style="margin-top: 8px;">
                <span class="{verdict_class}">{verdict_text}</span>
            </div>
            <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 8px;">
                Implied Upside: <span style="color: {'#10b981' if upside > 0 else '#ef4444'}; font-weight: 700;">
                {upside:+.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 2: VALUATION OUTPUT — THE THREE KEY NUMBERS
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💎</span>
        <h2>DCF Valuation Results</h2>
    </div>
    """, unsafe_allow_html=True)

    val_col1, val_col2, val_col3 = st.columns(3)

    with val_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Enterprise Value</div>
            <div class="metric-value">{format_large_number(dcf_result['enterprise_value'])}</div>
            <div class="metric-sub">PV of FCFs + Terminal Value</div>
        </div>
        """, unsafe_allow_html=True)

    with val_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Equity Value</div>
            <div class="metric-value green">{format_large_number(dcf_result['equity_value'])}</div>
            <div class="metric-sub">EV − Debt + Cash</div>
        </div>
        """, unsafe_allow_html=True)

    with val_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Intrinsic Value / Share</div>
            <div class="metric-value blue">{format_currency(dcf_result['per_share_value'])}</div>
            <div class="metric-sub">vs Market: {format_currency(current_price)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 3: KEY FINANCIAL DATA
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📋</span>
        <h2>Key Financial Metrics (TTM)</h2>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Revenue", format_large_number(data['revenue']))
    m2.metric("EBITDA", format_large_number(data['ebitda']))
    m3.metric("Free Cash Flow", format_large_number(data['fcf']))
    m4.metric("Net Income", format_large_number(data['net_income']))
    m5.metric("Beta", f"{data['beta']:.2f}")

    m6, m7, m8, m9, m10 = st.columns(5)
    m6.metric("Market Cap", format_large_number(data['market_cap']))
    m7.metric("Total Debt", format_large_number(data['total_debt']))
    m8.metric("Cash & Equiv.", format_large_number(data['total_cash']))
    m9.metric("Profit Margin", f"{data['profit_margin']*100:.1f}%")
    m10.metric("Rev Growth", f"{data['revenue_growth']*100:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 4: WACC BREAKDOWN
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📐</span>
        <h2>WACC Calculation Breakdown</h2>
    </div>
    """, unsafe_allow_html=True)

    wacc_col1, wacc_col2 = st.columns(2)

    with wacc_col1:
        st.markdown(f"""
        <div class="glass-panel">
            <h4 style="color: #818cf8; margin-bottom: 16px;">Cost of Equity (CAPM)</h4>
            <div style="color: #94a3b8; font-size: 0.9rem; line-height: 2;">
                <strong>Re = Rf + β × ERP</strong><br>
                Re = {risk_free_rate*100:.1f}% + {beta:.2f} × {equity_risk_premium*100:.1f}%<br>
                <strong style="color: #f1f5f9; font-size: 1.2rem;">
                    Cost of Equity = {cost_of_equity*100:.2f}%
                </strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with wacc_col2:
        st.markdown(f"""
        <div class="glass-panel">
            <h4 style="color: #a855f7; margin-bottom: 16px;">Weighted Average Cost of Capital</h4>
            <div style="color: #94a3b8; font-size: 0.9rem; line-height: 2;">
                <strong>WACC = (E/V)×Re + (D/V)×Rd×(1-T)</strong><br>
                WACC = {equity_weight*100:.1f}% × {cost_of_equity*100:.2f}% + {debt_weight*100:.1f}% × {cost_of_debt*100:.1f}% × (1 − {tax_rate*100:.0f}%)<br>
                <strong style="color: #f1f5f9; font-size: 1.2rem;">
                    WACC = {wacc*100:.2f}%
                </strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 5: PROJECTED FCF CHART
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📊</span>
        <h2>Projected Free Cash Flow</h2>
    </div>
    """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([3, 2])

    with chart_col1:
        # Build FCF projection chart
        years = [f"Year {i}" for i in range(1, projection_years + 1)]
        projected = dcf_result['projected_fcfs']
        discounted = dcf_result['discounted_fcfs']

        fig_fcf = go.Figure()

        # Projected FCF bars
        fig_fcf.add_trace(go.Bar(
            name='Projected FCF',
            x=years,
            y=[f / 1e9 for f in projected],
            marker_color='#6366f1',
            marker_line_width=0,
            opacity=0.9,
            text=[format_large_number(f) for f in projected],
            textposition='outside',
            textfont=dict(color='#94a3b8', size=10)
        ))

        # Discounted FCF bars
        fig_fcf.add_trace(go.Bar(
            name='Discounted FCF (PV)',
            x=years,
            y=[f / 1e9 for f in discounted],
            marker_color='#a855f7',
            marker_line_width=0,
            opacity=0.7,
            text=[format_large_number(f) for f in discounted],
            textposition='outside',
            textfont=dict(color='#94a3b8', size=10)
        ))

        fig_fcf.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#94a3b8'),
            barmode='group',
            height=400,
            margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=11)
            ),
            yaxis=dict(
                title='Billions ($)',
                gridcolor='rgba(255,255,255,0.05)',
                zeroline=False
            ),
            xaxis=dict(showgrid=False)
        )

        st.plotly_chart(fig_fcf, use_container_width=True)

    with chart_col2:
        # DCF Bridge / Waterfall Summary
        st.markdown(f"""
        <div class="glass-panel" style="height: 100%;">
            <h4 style="color: #06b6d4; margin-bottom: 20px;">DCF Bridge</h4>
            <div style="color: #94a3b8; line-height: 2.2; font-size: 0.9rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Base FCF (TTM)</span>
                    <strong style="color: #f1f5f9;">{format_large_number(fcf_base)}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>PV of Projected FCFs</span>
                    <strong style="color: #818cf8;">{format_large_number(dcf_result['pv_of_fcfs'])}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Terminal Value</span>
                    <strong style="color: #c084fc;">{format_large_number(dcf_result['terminal_value'])}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>PV of Terminal Value</span>
                    <strong style="color: #a855f7;">{format_large_number(dcf_result['discounted_terminal'])}</strong>
                </div>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 8px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Enterprise Value</span>
                    <strong style="color: #f1f5f9; font-size: 1.05rem;">{format_large_number(dcf_result['enterprise_value'])}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #ef4444;">− Total Debt</span>
                    <strong style="color: #ef4444;">({format_large_number(total_debt)})</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #10b981;">+ Cash & Equivalents</span>
                    <strong style="color: #10b981;">{format_large_number(total_cash)}</strong>
                </div>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 8px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span><strong>Equity Value</strong></span>
                    <strong style="color: #10b981; font-size: 1.1rem;">{format_large_number(dcf_result['equity_value'])}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>÷ Shares Outstanding</span>
                    <strong style="color: #f1f5f9;">{format_large_number(shares)}</strong>
                </div>
                <hr style="border-color: rgba(99,102,241,0.3); margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 1.1rem;">
                    <span><strong>Per-Share Value</strong></span>
                    <strong style="color: #22d3ee; font-size: 1.3rem;">{format_currency(per_share)}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 6: SENSITIVITY ANALYSIS HEAT MAP
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔥</span>
        <h2>Sensitivity Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;">
        This heat map shows how the <strong style="color: #f1f5f9;">Per-Share Intrinsic Value</strong> changes
        as WACC (x-axis) and Terminal Growth Rate (y-axis) vary. Cells highlighted in
        <strong style="color: #10b981;">green</strong> indicate the stock is undervalued relative to market price,
        while <strong style="color: #ef4444;">red</strong> indicates overvaluation.
    </div>
    """, unsafe_allow_html=True)

    # Generate sensitivity ranges centered around current assumptions
    wacc_center = wacc
    tg_center = terminal_growth

    wacc_range = [wacc_center + (i - 4) * 0.005 for i in range(9)]  # ±2% around WACC
    wacc_range = [max(0.01, w) for w in wacc_range]  # Ensure positive

    growth_range = [tg_center + (i - 4) * 0.005 for i in range(9)]  # ±2% around terminal growth
    growth_range = [max(0.001, g) for g in growth_range]  # Ensure positive

    # Filter: terminal growth must be less than all WACC values
    growth_range = [g for g in growth_range if g < min(wacc_range) - 0.005]
    if len(growth_range) < 3:
        growth_range = [0.01, 0.015, 0.02, 0.025, 0.03]
        growth_range = [g for g in growth_range if g < min(wacc_range)]

    sensitivity_df = generate_sensitivity_table(
        fcf_base=fcf_base,
        wacc_range=wacc_range,
        growth_range=growth_range,
        short_term_growth=short_term_growth,
        projection_years=projection_years,
        total_debt=total_debt,
        total_cash=total_cash,
        shares_outstanding=shares
    )

    # Create Plotly heatmap
    z_values = sensitivity_df.values
    x_labels = sensitivity_df.columns.tolist()
    y_labels = sensitivity_df.index.tolist()

    # Color based on whether above or below current price
    fig_heat = go.Figure(data=go.Heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale=[
            [0, '#ef4444'],      # Red (overvalued)
            [0.3, '#f59e0b'],    # Yellow
            [0.5, '#fbbf24'],    # Gold (near fair)
            [0.7, '#34d399'],    # Light green
            [1.0, '#10b981']     # Green (undervalued)
        ],
        text=[[f"${v:.2f}" for v in row] for row in z_values],
        texttemplate="%{text}",
        textfont=dict(size=11, color='white', family='Inter'),
        hoverongaps=False,
        hovertemplate="WACC: %{x}<br>Terminal Growth: %{y}<br>Per-Share Value: $%{z:.2f}<extra></extra>",
        colorbar=dict(
            title=dict(text='Per-Share Value ($)', font=dict(color='#94a3b8')),
            tickfont=dict(color='#94a3b8'),
            tickprefix='$'
        )
    ))

    fig_heat.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#94a3b8'),
        height=450,
        margin=dict(l=80, r=40, t=40, b=60),
        xaxis=dict(
            title='WACC',
            side='bottom',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title='Terminal Growth Rate',
            tickfont=dict(size=11)
        )
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Sensitivity Table (Expandable) ──
    with st.expander("📋 View Sensitivity Data Table"):
        # Style the dataframe
        styled_df = sensitivity_df.style.map(
            lambda v: f"color: #10b981; font-weight: 700" if v >= current_price else "color: #ef4444; font-weight: 700"
        ).format("${:.2f}")
        st.dataframe(styled_df, use_container_width=True)
        st.caption(f"**Green** = above current market price (${current_price:.2f}), **Red** = below market price")

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 7: HISTORICAL FINANCIALS CHART
    # ═══════════════════════════════════════════════════════════

    if data['hist_revenue']:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            <h2>Historical Revenue Trend</h2>
        </div>
        """, unsafe_allow_html=True)

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Bar(
            x=[str(y) for y in data['hist_years']],
            y=[r / 1e9 for r in data['hist_revenue']],
            marker_color='#6366f1',
            name='Revenue',
            text=[format_large_number(r) for r in data['hist_revenue']],
            textposition='outside',
            textfont=dict(color='#94a3b8', size=11)
        ))

        if data['hist_fcf'] and len(data['hist_fcf']) == len(data['hist_years']):
            fig_hist.add_trace(go.Scatter(
                x=[str(y) for y in data['hist_years']],
                y=[f / 1e9 for f in data['hist_fcf']],
                mode='lines+markers',
                name='Free Cash Flow',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8, color='#10b981')
            ))

        fig_hist.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#94a3b8'),
            height=350,
            margin=dict(l=40, r=20, t=20, b=40),
            yaxis=dict(
                title='Billions ($)',
                gridcolor='rgba(255,255,255,0.05)',
                zeroline=False
            ),
            xaxis=dict(showgrid=False),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 8: MODEL ASSUMPTIONS SUMMARY
    # ═══════════════════════════════════════════════════════════

    with st.expander("📖 Full Model Assumptions & Methodology"):
        st.markdown(f"""
        ### How This DCF Model Works

        **1. Data Source**
        - Financial data is pulled in real-time from Yahoo Finance via the `yfinance` library
        - Key inputs: Operating Cash Flow, Capital Expenditures, Total Debt, Cash, Shares Outstanding

        **2. Free Cash Flow (FCF)**
        - **FCF = Operating Cash Flow − Capital Expenditures**
        - Base FCF (TTM): **{format_large_number(fcf_base)}**

        **3. WACC Calculation (Capital Asset Pricing Model)**
        - **Cost of Equity** = Risk-Free Rate + Beta × Equity Risk Premium
        - Cost of Equity = {risk_free_rate*100:.1f}% + {beta:.2f} × {equity_risk_premium*100:.1f}% = **{cost_of_equity*100:.2f}%**
        - **WACC** = (E/V) × Re + (D/V) × Rd × (1 − Tax Rate)
        - Equity Weight: {equity_weight*100:.1f}% | Debt Weight: {debt_weight*100:.1f}%
        - **WACC = {wacc*100:.2f}%**

        **4. FCF Projections**
        - FCF is projected forward {projection_years} years at a **{short_term_growth*100:.1f}%** annual growth rate
        - This rate is based on historical performance and forward estimates

        **5. Terminal Value (Gordon Growth Model)**
        - TV = FCF_Year{projection_years} × (1 + g) / (WACC − g)
        - Terminal Growth Rate: **{terminal_growth*100:.1f}%** (approximates long-term GDP growth)
        - Terminal Value: **{format_large_number(dcf_result['terminal_value'])}**

        **6. Enterprise Value → Equity Value → Per-Share Value**
        - Enterprise Value = PV of projected FCFs + PV of Terminal Value = **{format_large_number(dcf_result['enterprise_value'])}**
        - Equity Value = EV − Total Debt + Cash = **{format_large_number(dcf_result['equity_value'])}**
        - Per-Share Value = Equity Value ÷ Shares Outstanding = **{format_currency(per_share)}**

        **7. Sensitivity Analysis**
        - The heat map shows how the per-share value changes across different WACC and Terminal Growth assumptions
        - This helps identify which variables have the greatest impact on valuation
        """)

    # ═══════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════

    st.markdown("""
    ---
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 16px 0;">
        <strong>Nexus Corporate Valuation Engine</strong> · MGMT 490AIFA · Spring 2026<br>
        Data sourced from Yahoo Finance · For educational purposes only · Not financial advice
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👈 Enter a ticker symbol in the sidebar and click **Run Valuation** to begin.")
