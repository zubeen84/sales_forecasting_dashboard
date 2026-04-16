# Sales Forecasting Dashboard
### Time series forecasting across three product categories with live interactive BI dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Prophet](https://img.shields.io/badge/Forecast-Prophet-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Governance](https://img.shields.io/badge/Design-ISO%2042001%20Aligned-742774?style=flat)

---

## Live Dashboard

[Open the live forecasting dashboard](https://salesforecastingdashboard-2rhmw5d3ejmqsnbxrbmu9j.streamlit.app/)

---

## At a Glance

| | |
|---|---|
| **Dataset** | Superstore Sales - 9,994 transactions across 4 years |
| **Scope** | Three product categories: Office Supplies, Furniture, Technology |
| **Models** | SARIMA (grid search, AIC-selected) and Facebook Prophet |
| **Forecast horizon** | 36 months with 95% confidence intervals |
| **Validation** | 6-month hold-out test window |
| **Accuracy** | SARIMA RMSE £332.37 - 3.3% of observed daily sales range |
| **Architecture** | Two-tier: analytical notebook + decoupled Streamlit dashboard |

---

## Overview

A validated sales forecasting solution delivering 36-month demand 
projections across three product categories, presented through an 
interactive business intelligence dashboard built with Streamlit 
and Plotly.

The goal is to support inventory planning, procurement decisions, 
and marketing strategy through accurate, interpretable forecasts 
validated on held-out data.

---

## Architecture

This project uses a deliberate two-tier architecture that reflects 
production data science practice.

### Tier 1 - Analytical layer (Jupyter Notebook)
- Exploratory data analysis and seasonal decomposition
- SARIMA model training with grid search hyperparameter tuning
- Facebook Prophet model training with uncertainty estimation
- Model validation on 6-month hold-out test window
- Forecast generation across 36-month horizon
- Results exported as structured CSV files

### Tier 2 - Presentation layer (Streamlit Dashboard)
- Loads pre-computed Prophet forecast CSVs at runtime
- Renders interactive Plotly visualisations with confidence intervals
- Category and horizon selection exposed to end users
- Business context and strategic recommendations applied

### Why pre-computed forecasts?

In production data environments, forecasting models run on a 
scheduled basis - nightly or weekly - and their outputs are 
persisted to a data store for downstream consumption by dashboards 
and reporting tools. Models are never executed live per user request.

This separation of concerns delivers three benefits:

**Performance:** Dashboard response times are sub-second regardless 
of model complexity.

**Reliability:** The presentation layer has no dependency on model 
runtime environments or Stan compiler availability. Deployment is 
clean and reproducible.

**Auditability:** Forecast outputs are versioned and stored 
independently of the dashboard. This supports ISO 42001 governance 
requirements. Forecasts can be reviewed, challenged, and traced 
back to their source model without re-running the pipeline.

This pattern mirrors architectures used in production BI platforms 
such as Tableau, Power BI, and Looker where the data model and 
presentation layer are always decoupled.

---

## Modelling Pipeline

### Data Preparation
- 9,994 transactions aggregated to monthly frequency per category
- Missing months imputed with category median
- Stationarity tested using Augmented Dickey-Fuller test

### SARIMA
- Grid search over (p,d,q)(P,D,Q,s) parameter space
- Model selected by minimising AIC across validation window
- Residual diagnostics: normality, autocorrelation, heteroscedasticity
- RMSE: £332.37 (3.3% of observed daily sales range)

### Facebook Prophet
- Additive seasonality with yearly components
- Automatic changepoint detection for trend shifts
- Uncertainty intervals at 95% confidence level
- Validated on 6-month hold-out window
- Forecast horizon: 36 months

### Model Selection Rationale
Both models were evaluated on the same hold-out window. Prophet was 
selected for the primary forecast output due to its superior handling 
of irregular seasonality and automatic uncertainty quantification, both critical for business planning applications.

---

## Key Results

| Category | Peak Month | Pattern | Planning Recommendation |
|----------|-----------|---------|------------------------|
| Office Supplies | December | Strong Q4 seasonality | Tactical Q3 stock build |
| Furniture | January | Stable upward trend | Long-term contracts |
| Technology | March | High volatility | Agile inventory management |

Confidence window: 6-12 months for operational decisions, 
24-36 months for strategic directional planning only.

---

## Dashboard Features

- Three product categories: Office Supplies, Furniture, Technology
- Four forecast horizons: 6, 12, 24 and 36 months
- Interactive Plotly charts with confidence interval shading
- Category-specific business recommendations
- Forecast summary metrics with delta indicators
- Mobile-responsive layout

---

## ISO 42001 AI Governance

This project applies ISO/IEC 42001:2023 AI Management System 
principles throughout:

**Transparency:** Methodology, model selection rationale, and 
uncertainty bands are fully visible. The two-tier architecture is 
documented so stakeholders understand how forecasts are generated.

**Accountability:** Forecast outputs are stored independently 
and can be audited without re-running the pipeline.

**Human oversight:** Forecasts are explicitly framed as planning 
inputs, not decisions. Recommendations are labelled as guidance 
requiring domain expertise to validate.

**Limitations disclosed:** Confidence intervals widen over longer 
horizons. Users are advised to use 6-12 month forecasts for 
operational decisions and treat 24-36 month outputs as strategic 
directional guidance only.

---

## Skills Demonstrated

`Python` `Facebook Prophet` `SARIMA` `Statsmodels` `Streamlit` `Plotly`  
`Time Series Analysis` `Seasonal Decomposition` `Stationarity Testing`  
`Augmented Dickey-Fuller` `Grid Search` `AIC Model Selection`  
`Holdout Validation` `Uncertainty Quantification` `Confidence Intervals`  
`Demand Forecasting` `Business Intelligence` `Dashboard Design`  
`Two-Tier Architecture` `Production ML Design` `ISO 42001` `Responsible AI`

---

## Run Locally

```bash
git clone https://github.com/zubeen84/sales_forecasting_dashboard.git
cd sales_forecasting_dashboard
pip install -r requirements.txt
streamlit run timeseries_app.py
```

---

## Related Projects

[Time Series Analysis Notebook](https://github.com/zubeen84/Time-Series-Sales-Analysis) 
- Full SARIMA and Prophet modelling pipeline (Part 1 of this project)

[Diabetes Risk Predictor](https://github.com/zubeen84/diabetes_risk_predictor) 
- Live ML classification app with ISO 42001 governance

---

## Disclaimer

Forecasts are generated from historical sales patterns and are 
provided for planning purposes only. They do not constitute 
financial or procurement advice. Always validate against current 
market conditions and domain expertise before making operational 
decisions.

---

## Author

**Zubeen Khalid**
MSc Applied Data Science Distinction - Anglia Ruskin University
ISO 42001 Certified | AI+ Foundation | Prompt Engineering Level 1

[LinkedIn](https://www.linkedin.com/in/zubeenkhalid) · 
[GitHub](https://github.com/zubeen84)
