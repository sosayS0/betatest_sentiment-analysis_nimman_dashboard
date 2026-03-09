Nimman Price Perception Insight (NPPI)
Quantifying the implicit value of restaurant attributes in Nimman, Chiang Mai — using customer reviews, OLS regression, and a multi-LLM benchmark for Thai-English sentiment analysis.

Senior Research Project · Faculty of Economics, Chiang Mai University · 2026


What this project does
Customers don't just pay for food. They pay for atmosphere, service, and the feeling that it was worth it. This project tries to put numbers on that.
By treating restaurant reviews as economic data, NPPI decomposes overall perceived value into attribute-level components — then asks which improvements actually move the needle on customer perception.
Two lenses are used:

Hedonic model — structured data (star ratings) → "which attribute drives overall rating the most?"
ABSA via LLM — unstructured text (review content) → "what do customers actually say they feel?"


Status
PhaseStatus1Data collection & engineering✅ Done2Hedonic regression modeling✅ Done3Gold standard annotation (100 reviews, 3 annotators)✅ Done4LLM benchmark — 10 models⏳ In progress5Dashboard🔜 Planned

Methodology
Phase 1 — Data

20,800+ reviews scraped from Google Maps and TripAdvisor across 72 restaurants in Nimman
Capped at 210 reviews per restaurant for corpus balance
Metadata: rating, date, platform, restaurant

Phase 2 — Hedonic Model
Applied Lancaster's Attribute Theory (1966) + OLS regression to quantify how much each attribute contributes to overall perceived value.
Avg_Rating = 0.148 + 0.298(Food) + 0.487(Service) + 0.184(Atmosphere) − 0.027(Price_Level)
R² = 0.81 · N = 72 restaurants
The β coefficients are read as relative importance weights — Service has the strongest marginal effect, followed by Food, then Atmosphere. Price Level was not significant (p = 0.23), likely due to the narrow range in this dataset.
Phase 3 — Gold Standard
Built a 100-review labeled dataset for evaluating LLM performance:

3 independent annotators labeled each review across 4 aspects (Food / Service / Atmosphere / Price) using POS · NEU · NEG · N/A
Inter-annotator agreement: Fleiss' κ = 0.73+ (Substantial, per Landis & Koch 1977)
Conflicts resolved by majority vote (54 cases) or lead researcher adjudication (2 cases), following SemEval ABSA conventions (Pontiki et al., 2014)

Label distribution:
AspectPOSNEGNEUN/AFood726715Service3512251Atmosphere466345Price144379
Phase 4 — LLM Benchmark (in progress)
10 models evaluated on the Gold Standard using identical prompts, temperature=0, via OpenRouter.
#ModelProviderTier1Gemini 2.5 FlashGoogle⚡ Fast2Gemini 2.5 ProGoogle💎 Flagship3GPT-4o miniOpenAI⚡ Fast4GPT-4oOpenAI💎 Flagship5Claude Haiku 4.5Anthropic⚡ Fast6Claude Sonnet 4.6Anthropic💎 Flagship7Llama 3.3 70BMetaOSS8Qwen 2.5 72BAlibabaOSS · Thai-best9DeepSeek V3.1DeepSeekOSS · MoE10DeepSeek R1DeepSeekOSS · Reasoning
Primary metric: Macro F1 per aspect. Also reporting Cohen's κ and confusion matrices.
Best model → applied to full 20,800+ review corpus to compute NASS (Nimman Aspect Sentiment Score) per restaurant.

Key findings so far

Service has the highest marginal effect on perceived value (β = 0.487) — more than Food or Atmosphere
Atmosphere had notably more annotator disagreement than other aspects (77% unanimous vs 94.9% for Price), reflecting how subjective ambience language tends to be
No model in this benchmark has published Thai-specific ABSA results — this experiment generates new data

(LLM benchmark results to be added after Phase 4)

Stack
ScrapingPython · BeautifulSoup / SeleniumProcessingPython · PandasModelingPython · statsmodelsAnnotation QAPython · sklearn (Fleiss' κ, Cohen's κ)LLM BenchmarkOpenRouter APIDashboardStreamlit (planned)

References

Lancaster, K. J. (1966). A new approach to consumer theory. Journal of Political Economy, 74(2), 132–157.
Pontiki, M. et al. (2014). SemEval-2014 Task 4: Aspect Based Sentiment Analysis. SemEval 2014.
Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, 33(1).


Tak Thongsoet · LinkedIn · GitHub
