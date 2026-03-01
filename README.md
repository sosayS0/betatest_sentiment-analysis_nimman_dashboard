# Nimman Price Perception Insight (NPPI)

> Quantifying the economic value of intangible restaurant attributes  
> through NLP and Hedonic Pricing Theory — Nimman, Chiang Mai.

---

## Overview

What makes customers *feel* a restaurant is worth the price?  
This project attempts to answer that question empirically.

NPPI is an independent research project that integrates **Data Science** with 
**Economics** to measure the "Shadow Price" of intangible attributes — service 
quality, atmosphere, and food experience — across restaurants in the Nimman 
district. The goal is to translate unstructured customer sentiment into 
actionable pricing intelligence for local entrepreneurs.

---

## Research Pipeline

### ✅ Phase 1 — Data Engineering (Completed)
Collected and cleaned **25,000+ customer reviews** from Google Maps and 
TripAdvisor via a custom Python scraping pipeline. Structured into an 
analysis-ready dataset with restaurant metadata, ratings, and raw review text.

### ⏳ Phase 2 — NLP & Sentiment Analysis (In Progress)
Applying a **DeBERTa-based transformer model** to classify review texts into 
distinct attribute categories (Food, Service, Atmosphere). Each review is 
decomposed into attribute-level sentiment scores, converting unstructured 
language into structured economic inputs.

### 📅 Phase 3 — Hedonic Pricing Model (Planned)
Using the sentiment scores as independent variables in a **Hedonic Pricing 
regression** to estimate the marginal contribution of each attribute to 
overall perceived value. Output: a replicable framework for shadow price 
estimation in the tourism sector.

### 📅 Phase 4 — Interactive Dashboard (Planned)
Findings will be presented via a **web-based dashboard** — designed to be 
accessible to non-technical business owners, not just analysts. The goal is 
to make the research outputs genuinely usable, not just academically interesting.

---

## Why This Project

Most pricing strategy advice for small restaurants is intuitive at best.  
This project is an attempt to put numbers on the things that are usually 
described in words — and make those numbers useful to the people running the 
businesses, not just the people studying them.

---

## Stack
- **Data Collection:** Python (Requests, BeautifulSoup / Selenium)
- **NLP:** DeBERTa (transformer-based sentiment classification)
- **Economic Modeling:** OLS Regression / Hedonic Pricing (Python / R)
- **Visualization:** TBD — targeting a lightweight, accessible web interface

---

## Status
`Phase 1 Complete` → `Phase 2 In Progress` → `Phase 3–4 Planned`

*Solo project. Part of undergraduate research at Chiang Mai University, 
Economics Department.*
