# 🎬 Video Script — Corporate Valuation Application Demo
### MGMT 490AIFA | Spring 2026 | ~9 Minutes
### Ticker: Apple Inc. (AAPL)

---

## SECTION 1: INTRODUCTION (1:00)

> *[Camera: Webcam visible. Screen shows the app's landing page with the "Corporate Valuation Engine" header.]*

**SAY:**

"Hey everyone. Today I'm going to walk you through a corporate valuation tool I built that performs a Discounted Cash Flow analysis on any publicly traded stock using real, live financial data.

So why does this matter? If you've ever tried to figure out what a stock is actually *worth* — not just what the market is pricing it at today — you know that static valuations go stale the moment market conditions change. Interest rates shift, a company's growth slows down, and suddenly that analyst price target from last quarter means nothing.

This tool solves that problem. It pulls real-time data directly from Yahoo Finance, lets you adjust every key assumption — WACC, growth rates, projection horizon — and instantly shows you how the intrinsic value changes. It's basically a stress-testing engine for your investment thesis.

Let me show you how it works using Apple — ticker AAPL."

---

## SECTION 2: BASE CASE DEMO (2:00)

> *[Screen: Navigate to the app. Type "AAPL" in the sidebar. Data loads automatically.]*

**SAY:**

"So here I've entered AAPL into the ticker input on the left sidebar, and the app immediately pulls Apple's live financial data from Yahoo Finance.

Up top, you can see the app identified this as **Apple Inc.**, in the **Technology** sector, **Consumer Electronics** industry. The current market price is showing **$264.18** per share.

Now, let's look at the three key outputs of our DCF model. These are the numbers that matter:

1. **Enterprise Value** — that's **$1.80 trillion**. This is the total value of the business before we account for the capital structure — it's the present value of all future projected free cash flows plus the terminal value.

2. **Equity Value** — **$1.77 trillion**. This is Enterprise Value minus total debt of about $90.5 billion, plus cash and equivalents of about $66.9 billion. This is what belongs to the shareholders.

3. **Intrinsic Value Per Share** — **$120.70**. This is the equity value divided by Apple's roughly 14.7 billion shares outstanding.

You can also see the app automatically compares this to the market price and gives a verdict. At $120.70 versus $264.18, that's an implied downside of about 54%, which the app flags as **Overvalued — Sell** with the default assumptions.

Now, that's a pretty dramatic number, and it's a great opportunity to talk about *why* — which comes down entirely to our assumptions. Let me walk through each one."

---

## SECTION 3: EXPLAIN ASSUMPTIONS (3:00)

### Part A — WACC Breakdown (~1:30)

> *[Screen: Scroll to the "WACC Calculation Breakdown" section. Point to each component.]*

**SAY:**

"The first and most important question: **How did I calculate WACC?**

WACC stands for Weighted Average Cost of Capital. It represents the blended rate of return a company needs to generate to satisfy both its debt holders and its equity investors. We use it as the discount rate in our DCF model.

The formula is:

**WACC = (E/V) × Cost of Equity + (D/V) × Cost of Debt × (1 − Tax Rate)**

Let me break down each piece.

For the **Cost of Equity**, I used the **Capital Asset Pricing Model**, or CAPM. The formula is:

**Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium**

Here are my specific inputs and where they come from:

- **Risk-Free Rate: 4.2%** — This is the current yield on the 10-Year U.S. Treasury bond. The 10-year Treasury is the standard proxy for a risk-free rate because it represents the return you'd get with essentially zero default risk.

- **Beta: 1.107** — This comes directly from Yahoo Finance. Beta measures Apple's volatility relative to the overall market. A beta of 1.1 means Apple moves roughly in line with the S&P 500, maybe slightly more volatile. This makes sense — Apple is a mega-cap with steady revenue, but it still has some cyclicality in hardware sales.

- **Equity Risk Premium: 5.5%** — This is the additional return investors expect for holding stocks instead of risk-free bonds. I'm using 5.5%, which is based on the long-term historical average excess return of the S&P 500 over Treasury bonds, consistent with estimates from Damodaran's annual ERP data.

So: Cost of Equity = 4.2% + 1.107 × 5.5% = **10.29%**.

For the **capital structure weights**, the app automatically calculates these from market data. Apple's equity weight is 97.7% and debt weight is just 2.3% — Apple has very little debt relative to its massive market cap.

For **Cost of Debt**, I'm using **4.5%** pre-tax, which approximates Apple's weighted average interest rate on outstanding bonds. After the **21% corporate tax rate** shield, that's about 3.6% after tax.

Putting it all together: WACC = 97.7% × 10.29% + 2.3% × 4.5% × (1 − 21%) = **10.14%**.

That 10.14% is the hurdle rate we'll use to discount all future cash flows back to today's dollars."

---

### Part B — Growth Rate Rationale (~0:45)

> *[Screen: Point to the growth rate sliders in the sidebar.]*

**SAY:**

"Next question: **Why this growth rate?**

I'm using an **8% short-term FCF growth rate** for the 5-year projection period. Here's my reasoning:

Apple's trailing twelve-month revenue growth is about **15.7%**, which is strong. However, that's boosted by iPhone 16 cycle tailwinds and AI-related features. Looking at their 3-to-5 year historical average, revenue growth is closer to 6-8%. Apple's Services segment — which includes the App Store, Apple Music, iCloud — is growing at roughly 14% annually and now makes up around 25% of revenue, which supports higher-than-GDP growth.

So 8% splits the difference between conservative historical averages and the optimistic analyst outlook. It accounts for continued Services momentum while recognizing that hardware growth will likely moderate.

For the **terminal growth rate**, I'm using **2.5%**. This represents the long-term sustainable growth rate after our projection period ends — it's meant to approximate nominal GDP growth. You never want this above 3-4% because no company can grow faster than the overall economy indefinitely."

---

### Part C — DCF Calculation Logic (~0:45)

> *[Screen: Scroll to the "DCF Bridge" panel and the Projected FCF chart.]*

**SAY:**

"Third question: **How does the DCF calculation actually work?** Let me trace the data step by step.

1. The app takes Apple's current **Free Cash Flow** — that's Operating Cash Flow of $135.5 billion minus Capital Expenditures, giving us a base FCF of about **$106.3 billion**.

2. It then **projects that FCF forward** 5 years at our 8% growth rate. So Year 1 is $114.8 billion, Year 2 is $124.0 billion, all the way to Year 5 at $156.2 billion.

3. For the **Terminal Value**, the app uses the Gordon Growth Model: it takes that final Year 5 cash flow, grows it one more year at our 2.5% terminal rate, and divides by (WACC minus terminal growth). That gives us a terminal value of about **$2.10 trillion** — this represents all cash flows from Year 6 to infinity.

4. Then it **discounts everything** back to present value using our 10.14% WACC. Each future dollar is worth less today because of the time value of money. The present value of the terminal value drops to **$1.29 trillion**.

5. Sum it all up: PV of projected FCFs plus PV of terminal value gives us **Enterprise Value of $1.80 trillion**.

6. Subtract debt, add back cash: **Equity Value of $1.77 trillion**.

7. Divide by 14.7 billion shares: **$120.70 per share**.

You can see all of this traced out in the DCF Bridge panel on the right side of the screen."

---

## SECTION 4: ADJUST ASSUMPTIONS — SCENARIO TESTING (2:00)

> *[Screen: Move to the sidebar sliders. Adjust them one at a time.]*

**SAY:**

"Now here's where this tool really shines — let's stress-test our assumptions and see what happens in real time.

**Scenario 1: Lower the WACC.**

Watch what happens when I bring the Risk-Free Rate down from 4.2% to, say, 3.0% — simulating a scenario where the Fed cuts rates. *(Adjust slider.)*

Look at that — the per-share value jumped significantly. A lower discount rate means future cash flows are worth more today. That's the power of interest rates on valuations — it's why growth stocks rally when the Fed signals rate cuts.

**Scenario 2: Increase the growth rate.**

Let me put the Risk-Free Rate back and instead bump the short-term growth rate from 8% up to 15% — maybe Apple's AI integration drives a massive Services expansion. *(Adjust slider.)*

You can see the intrinsic value climbing. More aggressive growth assumptions project larger future cash flows, which increases the present value.

**Scenario 3: Extend the projection period.**

Let me also move the projection period from 5 years to 8 years. *(Adjust slider.)*

This gives more weight to the high-growth period before we drop to the terminal rate, pushing the valuation higher.

The point here is that a DCF is only as good as its assumptions. Two analysts can look at the same company and get wildly different valuations just by tweaking WACC or growth by a percent or two. That's exactly why we need the sensitivity analysis."

> *[Reset sliders back to defaults: Rf=4.2%, Growth=8%, Terminal=2.5%, Years=5]*

---

## SECTION 5: SENSITIVITY ANALYSIS & CONCLUSION (2:00)

> *[Screen: Scroll down to the Sensitivity Analysis heatmap.]*

**SAY:**

"This brings us to the final and arguably most important section: **What does the sensitivity analysis show?**

This heat map is a two-dimensional table. On the **X-axis**, we have WACC — ranging from about 8.1% up to 12.1%. On the **Y-axis**, we have the Terminal Growth Rate — ranging from 0.5% to about 4.5%. Each cell shows what the **per-share intrinsic value** would be under that specific combination of assumptions.

A few key takeaways:

**First — the valuation is extremely sensitive to WACC.** Look across any single row. At a 2.5% terminal growth rate, moving WACC from 8.1% to 12.1% drops the per-share value from about $165 all the way down to roughly $95. That's a **$70 swing** from just a 4-percentage-point change in the discount rate. In fact, a 1% increase in WACC alone drops the per-share value by about **$14.55**. That tells us WACC is the single most impactful variable in this model.

**Second — terminal growth rate also matters, but less.** Reading down a single column, the range is narrower. Higher terminal growth assumptions push values up, but the effect is smaller than WACC changes. This makes sense — the terminal growth rate only affects cash flows beyond Year 5, while WACC discounts *every* cash flow.

**Third — under almost all scenarios in this table, Apple's intrinsic value comes in below the current market price of $264.** The green cells — representing scenarios where our model says the stock is undervalued — only appear at the most aggressive assumptions: very low WACC combined with very high terminal growth. Under our base case, and most reasonable variations, the DCF suggests Apple is trading at a premium to its intrinsic value.

**So what does this mean from an investment standpoint?**

Based on this analysis, with a WACC of 10.14% and 8% growth, Apple's per-share intrinsic value is about $120.70 versus a market price of $264. That's a significant premium. Now, this doesn't necessarily mean Apple is a bad investment — the market may be pricing in growth catalysts that our conservative assumptions don't capture, like the Apple Vision Pro ecosystem, AI integration across devices, or expansion into financial services.

But as a pure fundamentals-based DCF analysis, the data suggests that at $264, investors are paying a significant premium over what discounted cash flows alone would justify. My hypothetical recommendation would be a **Hold** for current shareholders, and I'd wait for a pullback before initiating a new position.

Thank you for watching. This has been a demonstration of the Nexus Corporate Valuation Engine for MGMT 490AIFA."

> *[Look at camera. Pause. End recording.]*

---

## 📋 RUBRIC CHECKLIST

| Question | Where It's Answered | Score Target |
|----------|-------------------|-------------|
| "How did you calculate WACC?" | Section 3A — Names Rf (4.2%, 10Y Treasury), Beta (1.107, Yahoo Finance), ERP (5.5%, historical avg), Cost of Debt (4.5%), Tax Rate (21%), capital structure weights from market data | ✅ Excellent |
| "Why this growth rate?" | Section 3B — References 15.7% trailing revenue growth, 3-5 year historical average, Services segment momentum, analyst outlook | ✅ Excellent |
| "How does your DCF calculation work?" | Section 3C — Walks through: FCF base → project forward → terminal value (Gordon Growth) → discount to PV → Enterprise Value → Equity Value → Per-Share | ✅ Excellent |
| "What does your sensitivity analysis show?" | Section 5 — Explains WACC has biggest impact ($14.55/share per 1%), terminal growth matters less, most scenarios show overvaluation, gives investment recommendation | ✅ Excellent |

---

## ⏱ TIMING GUIDE

| Section | Content | Target |
|---------|---------|--------|
| 1. Introduction | Problem statement, tool overview | 1:00 |
| 2. Base Case Demo | Enter AAPL, show 3 outputs | 2:00 |
| 3. Assumptions | WACC (1:30) + Growth (0:45) + DCF Logic (0:45) | 3:00 |
| 4. Scenario Testing | Adjust sliders, show real-time changes | 2:00 |
| 5. Sensitivity & Conclusion | Heatmap interpretation, investment recommendation | 2:00 |
| **TOTAL** | | **~10:00** |

---

## 💡 PRESENTATION TIPS

- **Look at the camera** when explaining the *why* (especially WACC rationale and growth justification)
- **Look at the screen** when pointing to specific numbers, charts, and sliders
- **Slow down** during Section 3 — this is worth the most points
- **Don't read the script word-for-word** — use it as a guide, speak naturally
- **Practice once or twice** to get timing right; aim for 9 minutes
- **Keep webcam visible** the entire time alongside your screen share
