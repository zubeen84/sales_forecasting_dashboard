# 📈 Sales Forecasting Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-brightgreen)
![Statsmodels](https://img.shields.io/badge/Forecast-Prophet-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Live App
👉 [Click here to open the dashboard](https://your-app-url.streamlit.app)

---

##  Overview

This project delivers a validated sales forecasting solution across 
three product categories: Office Supplies, Furniture and Technology 
using Facebook Prophet time series models. The analysis is presented 
through an interactive business intelligence dashboard built with 
Streamlit and Plotly.

The goal is to support strategic inventory planning, procurement 
decisions and marketing strategy through accurate, interpretable 
36-month forecasts validated on a 6-month hold-out test window.

---

##  Architecture - Notebook vs Dashboard

This project follows a **two-tier architecture** that reflects 
real-world production data science practice:

### Tier 1: Analytical Layer (Jupyter Notebook)
The full modelling pipeline runs in the notebook:

- Exploratory data analysis and seasonal decomposition
- SARIMA model training with hyperparameter tuning
- Facebook Prophet model training with uncertainty estimation
- Model validation on 6-month hold-out test window
- Forecast generation across 36-month horizon
- Results exported as structured CSV files

### Tier 2: Presentation Layer (Streamlit Dashboard)
The dashboard consumes pre-computed forecast outputs:

- Loads Prophet forecast CSVs at runtime
- Renders interactive Plotly visualisations
- Applies business context and strategic recommendations
- Exposes category and horizon selection to end users

### Why Pre-Computed Forecasts?

This architecture is a deliberate design decision aligned with 
production best practices not a technical workaround.

In enterprise data environments, forecasting models are computationally 
intensive and are never executed live per user request. Instead they 
run on a scheduled basis, typically nightly or weekly and their 
outputs are persisted to a data store for downstream consumption by 
dashboards and reporting tools.

This separation of concerns delivers three key benefits:

**1. Performance**  Dashboard response times are sub-second 
regardless of model complexity. Users are never waiting for a model 
to train.

**2. Reliability**  The presentation layer has no dependency on 
model runtime environments or Stan compiler availability. Deployment 
is clean and reproducible across any cloud environment.

**3. Auditability**  Forecast outputs are versioned and stored 
independently of the dashboard. This supports governance requirements 
under ISO 42001 as forecasts can be reviewed, challenged and traced 
back to their source model without re-running the pipeline.

This pattern mirrors architectures used in production BI platforms 
such as Tableau, Power BI and Looker where the data model and 
the presentation layer are always decoupled.

---

##  Modelling Pipeline

### Data Preparation
- Dataset: Superstore Sales consisiting of 9,994 transactions across 4 years
- Aggregated to monthly frequency per category
- Missing months imputed with category median
- Stationarity tested using Augmented Dickey-Fuller test

### SARIMA Model
- Grid search over (p,d,q)(P,D,Q,s) parameter space
- Selected by minimising AIC across validation window
- Residual diagnostics: normality, autocorrelation, heteroscedasticity
- **RMSE: £332.37 [3.3% of observed daily sales range]**

### Facebook Prophet Model
- Additive seasonality with yearly components
- Automatic changepoint detection for trend shifts
- Uncertainty intervals at 95% confidence level
- Validated on 6-month hold-out test window
- Forecast horizon: 36 months

### Model Selection Rationale
Both SARIMA and Prophet were evaluated on the same hold-out window. 
Prophet was selected for the primary forecast output due to its 
superior handling of irregular seasonality and automatic uncertainty 
quantification both critical for business planning applications.

---

## Key Results

| Category | Peak Month | Pattern | Planning Recommendation |
|----------|-----------|---------|------------------------|
| Office Supplies | December | Strong Q4 seasonality | Tactical Q3 stock build |
| Furniture | January | Stable upward trend | Long-term contracts |
| Technology | March | High volatility | Agile inventory management |

**SARIMA Forecast Accuracy:**
- RMSE: £332.37
- Forecast error: 3.3% of observed daily sales range
- Validated on: 6-month hold-out test window
- Confidence window: 6-12 months operational, 24-36 months strategic

---

## Dashboard Features

-  Three product categories: Office Supplies, Furniture, Technology
-  Four forecast horizons: 6, 12, 24 and 36 months
-  Interactive Plotly charts with confidence interval shading
-  Category-specific business recommendations
-  Forecast summary metrics with delta indicators
-  ISO 42001 governance principles applied throughout
-  Mobile responsive layout

---

## 🏛️ ISO 42001 AI Governance

This dashboard is built in alignment with 
**ISO/IEC 42001:2023 - AI Management Systems:**

✅ **Transparency:**
Forecasting methodology, model selection rationale and uncertainty 
bands are fully visible to users. The two-tier architecture is 
documented so stakeholders understand exactly how forecasts 
are generated.

✅ **Accountability:**
Clear authorship, data provenance and model versioning. Forecast 
outputs are stored independently so they can be audited and 
challenged without re-running the pipeline.

✅ **Fairness:**
No demographic or protected characteristics are used in the model. 
Forecasts are derived purely from historical sales patterns.

✅ **Human Oversight:**
The dashboard explicitly frames forecasts as planning inputs not 
decisions. Business recommendations are clearly labelled as guidance 
requiring domain expertise and market knowledge to validate.

✅ **Limitations Disclosed:**
Confidence intervals widen over longer horizons. Users are advised 
to use 6–12 month forecasts for operational decisions and treat 
24–36 month forecasts as strategic directional guidance only.

---

##  How to Run Locally
```bash
git clone https://github.com/zubeen84/sales_forecasting_dashboard.git
cd sales_forecasting_dashboard
pip install -r requirements.txt
streamlit run timeseries_app.py
---
---

##  Related Projects

📓 [Time Series Analysis Notebook](https://github.com/zubeen84/Time-Series-Sales-Analysis) - full SARIMA and Prophet modelling pipeline

🩺 [Diabetes Risk Predictor](https://github.com/zubeen84/diabetes-risk-predictor) - live ML classification app with ISO 42001 governance

---

## ⚠️ Disclaimer

Forecasts are generated from historical sales patterns and are 
provided for planning purposes only. They do not constitute 
financial advice. Always validate forecasts against current 
market conditions and domain expertise before making procurement 
or inventory decisions.

---

## 👤 Author

**Zubeen Khalid**
MSc Applied Data Science
🏛️ ISO 42001 Certified AI Governance
🔗 [LinkedIn](https://www.linkedin.com/in/zubeenkhalid)
🐙 [GitHub](https://github.com/zubeen84)
