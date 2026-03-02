# Nimman Price Perception Insight (NPPI)

**A data-driven economic research project quantifying the "Shadow Price" of 
intangible restaurant attributes in Nimman, Chiang Mai — integrating LLM-powered 
NLP with Hedonic Pricing Theory to generate actionable pricing intelligence for 
the local tourism and F&B sector.**

---

## Overview

Customers don't just pay for food — they pay for atmosphere, service, and 
perceived value. But how much is each of those *actually* worth?

This project uses customer review data and economic modeling to answer that 
question with numbers. By applying Hedonic Pricing Theory, NPPI decomposes a 
restaurant's overall perceived value into measurable, attribute-level components 
— giving local entrepreneurs a framework to prioritize improvements that yield 
the highest marginal returns.

---

## Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Data Collection & Engineering | ✅ Complete |
| 2 | LLM-Powered Sentiment Analysis | ✅ Complete |
| 3 | Hedonic Regression Modeling | ✅ Complete |
| 4 | Dashboard & Visualization | ⏳ In Progress |

---

## Methodology

### Phase 1 — Data Engineering
- Scraped and cleaned **25,000+ customer reviews** from Google Maps and Tripadvisor 
  covering restaurants in the Nimman area
- Structured raw text data into an analysis-ready dataset with metadata 
  (rating, date, platform, restaurant category)

### Phase 2 — LLM-Powered Sentiment Analysis
- Used the **Gemini 2.5 Flash API** to classify review text into distinct 
  business attribute dimensions: **Food Quality, Service, Atmosphere, and Price-Value**
- Extracted attribute-level sentiment scores from unstructured text at scale, 
  without relying on traditional NLP libraries

> *Choosing an API-based LLM over a fine-tuned model was a deliberate tradeoff: 
> faster iteration, lower infrastructure overhead, and strong out-of-the-box 
> performance on Thai-English mixed review text.*

### Phase 3 — Hedonic Pricing Model
- Applied **Hedonic Regression** to quantify the marginal contribution of each 
  attribute to overall perceived value (as proxied by star ratings)
- Identified which attribute improvements yield the **highest shadow price** — 
  i.e., the biggest perceived value gain per unit of improvement
- Outputs a ranked priority framework for pricing strategy and business 
  investment decisions

### Phase 4 — Dashboard (In Progress)
- Building an interactive visualization layer using **Streamlit** to present 
  findings accessibly to non-technical stakeholders (restaurant owners, 
  local entrepreneurs)
- Planned deployment via Streamlit Cloud

---

## Key Concepts

**Hedonic Pricing Theory** — An economic method that treats a product's price 
as a function of its individual characteristics. Applied here to perceived value 
rather than market price, allowing us to isolate the contribution of intangibles 
like "atmosphere" that don't appear on any balance sheet.

**Shadow Price** — The implicit economic value assigned to an attribute that 
has no direct market price. In this context: how much extra perceived value 
does a one-unit improvement in service quality generate?

---

## Tech Stack

- **Data Collection:** Python (requests, BeautifulSoup / Selenium)
- **Data Processing:** Python (Pandas)
- **Sentiment Analysis:** Gemini 2.5 Flash API
- **Economic Modeling:** Python (statsmodels / scipy)
- **Visualization:** Streamlit *(in progress)*

---

## Selected Finding (Preview)

> Atmosphere had a disproportionately high shadow price relative to its 
> improvement cost among mid-tier restaurants — suggesting it is systematically 
> underinvested in compared to food quality.

*(Full results and interactive dashboard coming soon)*

---

## About

**Tak Thongsoet** — Economics & Data Analysis  
Chiang Mai University | Bachelor of Economics (Marketing Minor)  

This project was selected as a featured project on the Digital Solutions Lab 
website for integrating Economics with Data Science.

[LinkedIn](https://www.linkedin.com/in/tak-thongsoet) · 
[GitHub](https://github.com/sosayS0)
