# Nimman Price Perception Insight (NPPI)

A data-driven research project quantifying the **"Shadow Price"** of intangible 
restaurant attributes — service quality, atmosphere, and food experience — in 
Chiang Mai's Nimman dining district.

The project bridges **Economics (Hedonic Pricing Theory)** and **Data Science (NLP 
sentiment analysis)** to deliver actionable pricing intelligence for local entrepreneurs 
and tourism stakeholders.

---

## Project Overview

Consumers don't just pay for food — they pay for *perceived value*. This project 
attempts to measure exactly how much each intangible attribute contributes to that 
perception, and which improvements yield the highest marginal returns.

---

## Methodology

**Phase 1 — Data Engineering** ✅  
Collected and cleaned 25,000+ customer reviews from Google Maps and TripAdvisor 
via a custom Python scraping pipeline. Structured into analysis-ready datasets 
with restaurant metadata and price-tier classifications.

**Phase 2 — NLP Sentiment Pipeline** ✅  
Deployed a DeBERTa-based NLP model to classify unstructured review text into 
distinct attribute dimensions: Food, Service, and Atmosphere. Output: per-restaurant 
attribute sentiment scores used as independent variables in economic modeling.

**Phase 3 — Hedonic Pricing Model** ✅  
Applied regression-based Hedonic Pricing Models to quantify the marginal contribution 
of each attribute to overall perceived value. Identifies which attribute investments 
deliver the highest return — actionable intelligence for pricing strategy decisions.

**Phase 4 — Visualization & Deployment** ⏳  
Building an interactive dashboard to present findings to non-technical stakeholders, 
including restaurant owners and tourism policymakers.

---

## Stack

- **Python** — data collection, cleaning, NLP orchestration, modeling  
- **Hedonic Pricing / OLS Regression** — economic modeling  
- **Pandas, Scikit-learn** — data processing and statistical analysis  
- **Visualization** — in progress

---

## Status

Core research pipeline complete. Visualization and public deployment in progress.
