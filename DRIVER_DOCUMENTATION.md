# DRIVER Documentation — Corporate Valuation Engine (DCF Model)
### MGMT 490AIFA | Spring 2026

---

## D — DISCOVER & DEFINE

### What Problem Are We Solving?
Static stock valuations go stale the moment market conditions change. Analysts publish price targets based on assumptions that may no longer hold — interest rates shift, growth slows, debt changes. Individual investors and students need a way to dynamically value a company and stress-test their assumptions in real time.

### Objective
Build an interactive Discounted Cash Flow (DCF) valuation tool that:
- Pulls **live financial data** from Yahoo Finance for any US-traded stock
- Calculates **intrinsic value per share** using industry-standard methods (CAPM → WACC → DCF)
- Allows users to **adjust every key assumption** (risk-free rate, beta, growth rates, projection period) and see results update instantly
- Includes a **sensitivity analysis** to visualize how valuation changes across assumption scenarios
- Provides a clear **Buy / Hold / Sell** verdict by comparing intrinsic value to market price

### Success Criteria
- A working web application that accepts any ticker and produces a defensible valuation
- Ability to explain **why** each assumption was chosen (not just what the numbers are)
- Sensitivity analysis that reveals which assumptions have the greatest impact
- Stable across different tickers with varying financial profiles

### Resources & Constraints
- **Data Source:** Yahoo Finance via the `yfinance` Python library (free, no API key required)
- **Tech Stack:** Python, Streamlit (UI framework), Plotly (visualization), NumPy/Pandas (calculations)
- **Constraints:** Must work locally and be deployable without cost; educational use only — not financial advice
- **Knowledge Foundation:** Understanding of time value of money, CAPM, WACC, and DCF from coursework

### Key Questions Before Proceeding
- Where does each WACC input come from, and what makes each reasonable?
- What growth rate is defensible for a specific company, and why?
- How sensitive is the final valuation to each assumption?
- How do we handle edge cases (negative FCF, missing data, unusual capital structures)?

---

## R — REPRESENT

### Architecture & Data Flow

```
User Input (Ticker) 
    → Yahoo Finance API (yfinance)
        → Raw Financial Data (Revenue, FCF, Beta, Debt, Cash, Shares)
            → CAPM Calculation (Rf + β × ERP = Cost of Equity)
                → WACC Calculation (Equity weight × CoE + Debt weight × CoD × (1-Tax))
                    → FCF Projection (Base FCF × (1 + growth)^n for each year)
                        → Terminal Value (Gordon Growth Model)
                            → Discount All Cash Flows to Present Value
                                → Enterprise Value (Sum of PV of FCFs + PV of Terminal Value)
                                    → Equity Value (EV − Debt + Cash)
                                        → Per-Share Intrinsic Value (Equity Value ÷ Shares)
                                            → Compare to Market Price → Buy/Hold/Sell Verdict
```

### Application Layout Plan

| Section | Purpose |
|---------|---------|
| **Sidebar** | Ticker input, WACC component sliders, growth rate sliders, projection period, quick ticker buttons, refresh data |
| **Hero** | Company name, sector, current market price, intrinsic value verdict |
| **DCF Results** | Enterprise Value, Equity Value, Per-Share Value cards |
| **Key Metrics** | TTM Revenue, EBITDA, FCF, Net Income, Beta, Market Cap, Debt, Cash |
| **WACC Breakdown** | Step-by-step CAPM → WACC calculation with current inputs |
| **Projected FCF Chart** | Bar chart of projected and discounted FCFs over projection period |
| **DCF Bridge** | Waterfall showing EV → subtract debt → add cash → Equity Value |
| **Sensitivity Heatmap** | WACC vs. Terminal Growth Rate matrix, color-coded relative to market price |
| **Historical Trends** | Revenue and FCF over past 4 years |
| **Full Methodology** | Expandable section explaining all formulas and assumptions |

### Key Design Decisions
1. **CAPM for Cost of Equity** — industry-standard, uses observable inputs (Treasury yield, Beta, ERP)
2. **Gordon Growth Model for Terminal Value** — appropriate for mature companies with stable growth
3. **Sensitivity Analysis** — two most impactful variables (WACC and Terminal Growth Rate) as axes
4. **Color-coded heatmap** — green = undervalued relative to market price, red = overvalued

---

## I — IMPLEMENT

### What Was Built

**1. Data Layer (`fetch_financial_data` function)**
- Fetches all financial data from Yahoo Finance using `yfinance`
- Extracts: current price, beta, revenue, EBITDA, FCF, operating cash flow, CapEx, debt, cash, shares outstanding, market cap, profit margins, revenue growth
- Cached for 60 seconds with `@st.cache_data(ttl=60)` to balance freshness with API rate limits
- "Refresh Data" button clears cache and forces fresh API call using a timestamped cache key

**2. WACC Engine (`calculate_wacc` function)**
- Implements CAPM: `Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium`
- Calculates capital structure weights from market cap and total debt
- Applies tax shield to cost of debt: `After-tax CoD = Cost of Debt × (1 - Tax Rate)`
- Computes WACC: `WACC = (E/V) × CoE + (D/V) × CoD × (1 - Tax)`

**3. DCF Engine (`run_dcf` function)**
- Projects FCF forward for N years at the user-specified growth rate
- Calculates Terminal Value using Gordon Growth Model: `TV = FCF_final × (1 + g) / (WACC - g)`
- Discounts each projected FCF and terminal value to present value using WACC
- Derives: Enterprise Value → Equity Value (EV - Debt + Cash) → Per-Share Value

**4. Sensitivity Analysis (`generate_sensitivity_table` function)**
- Creates a matrix of per-share values across WACC range (±2% from base) and terminal growth range (0.5% to 4.5%)
- Colors dynamically pivot around current market price — all-red when all scenarios show overvaluation, green only when intrinsic value exceeds market price

**5. Interactive UI (Streamlit)**
- Sidebar with sliders for every adjustable input
- Real-time recalculation on any input change
- Quick Ticker buttons for popular stocks
- Professional dark theme with glassmorphism effects

### AI Usage in Implementation
- AI assisted with generating the Streamlit UI structure, Plotly chart configurations, and CSS styling
- All financial logic (CAPM, WACC, DCF, Gordon Growth Model) was understood and verified manually before coding
- I verified every calculation against hand-computed examples (see Validate section)
- AI helped debug edge cases: handling tickers with missing CapEx data, negative FCF warnings, division-by-zero protection when WACC approaches terminal growth rate

### Key Decisions During Implementation
- **R-I Loop #1:** Initially planned a static report. Realized during implementation that interactive sliders would be far more educational — went back to REPRESENT and redesigned for real-time interactivity.
- **R-I Loop #2:** Originally used a simple min/max color scale for the heatmap. Realized this was misleading (showing green for values still below market price). Went back and redesigned colors to pivot around the actual market price.
- **R-I Loop #3:** Started with 5-minute data cache. Realized during demo that stale data was confusing — reduced to 60 seconds and added a manual refresh button with timestamp.

---

## V — VALIDATE

### Numerical Verification (Apple — AAPL)
Spot-checked the model by hand-calculating three cells from the sensitivity table:

| Scenario | Hand Calculation | App Output | Match? |
|----------|-----------------|------------|--------|
| WACC=8.2%, TG=2.5% | $163.42 | $163.92 | ✅ (within rounding) |
| WACC=10.2%, TG=2.5% | $119.64 | $119.91 | ✅ |
| WACC=12.2%, TG=0.5% | $82.13 | $82.26 | ✅ |

### Directional Checks
- ✅ Lowering WACC increases valuation (less discounting)
- ✅ Raising growth rate increases valuation (larger future cash flows)
- ✅ Extending projection period increases valuation (more high-growth years before terminal rate)
- ✅ Higher beta → higher WACC → lower valuation

### Edge Case Testing
- ✅ Tested tickers with negative FCF — app displays warning and handles gracefully
- ✅ Terminal growth rate approaching WACC — model caps to prevent infinity/negative terminal values
- ✅ Tickers with missing data fields — app uses fallbacks (e.g., calculates FCF from Operating CF - CapEx when direct FCF is unavailable)

### Reasonableness Checks
- ✅ Enterprise Value for Apple ($1.80T) is below market cap ($3.88T) — consistent with typical DCF conservatism using moderate assumptions
- ✅ WACC of 10.14% for Apple is reasonable for a tech mega-cap with low debt and beta ~1.1
- ✅ Terminal value represents ~72% of total enterprise value — within the typical 60-80% range for DCF models

### Data Source Validation
- ✅ yfinance pulls from Yahoo Finance, which sources from SEC filings (10-K, 10-Q) and real-time market feeds
- ✅ Compared key metrics (revenue, FCF, debt) against Apple's most recent 10-K filing — all consistent

---

## E — EVOLVE

### Improvements Made During Development
1. **Data Freshness:** Reduced cache TTL from 5 minutes to 60 seconds; added manual refresh button with timestamp
2. **Heatmap Colors:** Pivoted from static gradient to market-price-relative coloring — green only appears when a scenario shows undervaluation
3. **Sidebar Readability:** Made all sidebar text white for readability on dark background; gave Quick Ticker buttons gray backgrounds
4. **Deprecation Fixes:** Updated `Styler.applymap` → `Styler.map` to eliminate console warnings
5. **Historical Chart Legend:** Made legend text white for visibility on dark background
6. **Expander Sections:** Made methodology text white for readability

### Potential Future Enhancements
- **Alternative Terminal Value Method:** Add EV/EBITDA exit multiple approach alongside Gordon Growth Model
- **Monte Carlo Simulation:** Randomize inputs across distributions to show probability-weighted outcomes
- **Multi-Company Comparison:** Compare intrinsic values across competitors side-by-side
- **Export to PDF:** Allow users to download a formatted valuation report
- **Deployed Version:** Host on Streamlit Community Cloud for browser-based access without Python

### Reusable Patterns
- `@st.cache_data` with a `_refresh_key` parameter pattern for manual cache busting
- Dynamic colorscale normalization relative to a reference value (market price)
- Sidebar-controlled real-time recalculation pattern for financial models

---

## R — REFLECT

### What Worked Well
1. **Interactive sliders changed everything.** Being able to adjust WACC and see the valuation move in real time makes the relationship between assumptions and outcomes visceral rather than abstract.
2. **The sensitivity heatmap is the most valuable output.** It immediately shows that WACC dominates the valuation — a 1% change swings per-share value by ~$15. This is more insightful than any single-point estimate.
3. **Starting with hand calculations before coding** ensured I understood the math. When the app produced numbers, I could verify them because I already knew what to expect.
4. **The R-I loop was constant.** The plan changed at least three times during implementation (interactivity, heatmap colors, data freshness). Each loop improved the product.

### What I Would Do Differently
1. **Start with the sensitivity analysis, not the single-point DCF.** The heatmap is the real deliverable — the base case is just one cell in the table. I should have designed around that insight from the start.
2. **Test more tickers earlier.** Some edge cases (negative FCF, missing data) only surfaced late. Earlier cross-ticker testing would have caught these sooner.
3. **Document assumptions in the app from Day 1.** The methodology section was added last, but it should be baked into the design from the beginning.

### Key Takeaways
1. **A DCF is only as good as its assumptions.** The model itself is deterministic — the uncertainty lives entirely in the inputs (WACC, growth rate, terminal growth). This is why sensitivity analysis matters more than the base case.
2. **WACC is the most powerful lever.** Across all tickers tested, WACC changes produced the largest valuation swings. This aligns with theory — WACC discounts every cash flow, while growth only affects projected and terminal cash flows.
3. **The market price contains information the DCF doesn't capture.** Apple's DCF value ($120) is far below market ($264), but the market prices in growth optionality (AI, Vision Pro, Services expansion) that a backward-looking DCF can't quantify. Neither is "wrong" — they're answering different questions.
4. **AI is a force multiplier, not a replacement.** AI helped build the UI and debug edge cases faster. But understanding *why* WACC = 10.14% and *why* 8% growth is defensible — that's human judgment grounded in financial knowledge. AI can generate the code; you have to generate the conviction.

### Transferable Insights
- The pattern of "compute a model → visualize sensitivity to inputs" applies to any quantitative decision (pricing models, project finance, risk assessment)
- Color-coding relative to a meaningful reference point (market price) is more informative than arbitrary gradients
- Interactive tools teach better than static reports because they let the user explore "what if" questions on their own terms

---

*This DRIVER documentation was produced as part of the Corporate Valuation Engine project for MGMT 490AIFA, Spring 2026.*
