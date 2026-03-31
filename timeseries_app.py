import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_forecasts():
    data = {}
    categories = {
        "Office Supplies": "office_supplies",
        "Furniture": "furniture",
        "Technology": "technology"
    }
    for name, filename in categories.items():
        history = pd.read_csv(
            f"forecasts/{filename}_history.csv",
            parse_dates=["ds"]
        )
        forecast = pd.read_csv(
            f"forecasts/{filename}_forecast.csv",
            parse_dates=["ds"]
        )
        data[name] = {
            "history": history,
            "forecast": forecast
        }
    return data

data = load_forecasts()

insights = {
    "Office Supplies": {
        "pattern": "Strong Q4 seasonal spikes",
        "recommendation": "Increase stock in Q3 ahead of Q4 surge",
        "risk": "Low - predictable seasonal demand"
    },
    "Furniture": {
        "pattern": "Stable upward growth trend",
        "recommendation": "Suitable for long-term procurement contracts",
        "risk": "Low - consistent demand pattern"
    },
    "Technology": {
        "pattern": "High volatility with unpredictable spikes",
        "recommendation": "Maintain flexible inventory and agile marketing",
        "risk": "High - demand spikes are hard to predict"
    }
}

st.title("Sales Forecasting Dashboard")
st.write("Interactive sales forecasting across product categories using Facebook Prophet.")
st.info("Designed for business analysts and strategic planners. Forecasts are pre-computed from Prophet models and updated on a scheduled basis reflecting production BI best practice.")
st.divider()

with st.sidebar:
    st.header("Dashboard Settings")
    st.divider()

    category = st.selectbox(
        "Select Category:",
        ["Office Supplies", "Furniture", "Technology"]
    )

    horizon = st.selectbox(
        "Forecast Horizon:",
        [6, 12, 24, 36],
        format_func=lambda x: f"{x} months"
    )

    st.divider()
    st.subheader("Category Insights")
    info = insights[category]
    st.write(f"**Pattern:** {info['pattern']}")
    st.write(f"**Recommendation:** {info['recommendation']}")
    st.write(f"**Risk Level:** {info['risk']}")

    st.divider()
    st.subheader("Forecasting Method")
    st.write("**Model:** Facebook Prophet")
    st.write("**Seasonality:** Yearly additive")
    st.write("**Confidence:** 95% intervals")
    st.write("**Horizon:** 36 months")
    st.write("**Validation:** 6-month hold-out window")

    st.divider()
    st.subheader("🏛️ ISO 42001 Governance")
    st.write("✅ **Transparency** - method and uncertainty bands visible")
    st.write("✅ **Accountability** - authorship and data source stated")
    st.write("✅ **Auditability** - forecasts versioned independently")
    st.write("✅ **Limitations** - confidence decreases over longer horizons")
    st.divider()
    st.warning("⚠️ Forecasts are for planning purposes only. Always combine with domain expertise and market knowledge.")
    st.divider()
    st.write("Built by **Zubeen Khalid**")
    st.write("MSc Applied Data Science")
    st.write("🏛️ ISO 42001 AI Governance")

history = data[category]["history"]
forecast = data[category]["forecast"]
last_actual_date = history["ds"].max()
forecast_only = forecast[
    forecast["ds"] > last_actual_date
].head(horizon)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Total Historical Sales",
        f"£{history['y'].sum():,.0f}"
    )
with col2:
    st.metric(
        "Avg Monthly Sales",
        f"£{history['y'].mean():,.0f}"
    )
with col3:
    st.metric(
        "Peak Month Sales",
        f"£{history['y'].max():,.0f}"
    )

st.divider()
st.subheader(f" {category} - {horizon} Month Forecast")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=history["ds"],
    y=history["y"],
    mode="lines+markers",
    name="Actual Sales",
    line=dict(color="#00C9A7", width=2),
    marker=dict(size=4)
))

fig.add_trace(go.Scatter(
    x=forecast_only["ds"],
    y=forecast_only["yhat"],
    mode="lines",
    name="Prophet Forecast",
    line=dict(color="#845EF7", width=2, dash="dash")
))

fig.add_trace(go.Scatter(
    x=forecast_only["ds"],
    y=forecast_only["yhat_upper"],
    mode="lines",
    name="Upper Bound",
    line=dict(width=0),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=forecast_only["ds"],
    y=forecast_only["yhat_lower"],
    mode="lines",
    name="95% Confidence Interval",
    fill="tonexty",
    fillcolor="rgba(132, 94, 247, 0.15)",
    line=dict(width=0)
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales (£)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    plot_bgcolor="#F8FAFC",
    paper_bgcolor="#F8FAFC",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, width="stretch")

st.divider()
st.subheader("Forecast Summary")

col4, col5, col6 = st.columns(3)
last_actual = history["y"].iloc[-1]
next_forecast = forecast_only["yhat"].iloc[0]
end_forecast = forecast_only["yhat"].iloc[-1]
change = next_forecast - last_actual

with col4:
    st.metric(
        "Last Actual Month",
        f"£{last_actual:,.0f}"
    )
with col5:
    st.metric(
        "Next Month Forecast",
        f"£{next_forecast:,.0f}",
        delta=f"£{change:,.0f}"
    )
with col6:
    st.metric(
        f"Month {horizon} Forecast",
        f"£{end_forecast:,.0f}"
    )

st.divider()
st.subheader("💼 Business Recommendation")
st.success(
    f"**{category}:** {insights[category]['recommendation']}"
)
st.write(f"**Demand Pattern:** {insights[category]['pattern']}")
st.write(f"**Planning Risk:** {insights[category]['risk']}")
st.write("**Note:** Confidence intervals widen over longer horizons. Use 6-12 month forecasts for operational decisions and 24-36 month forecasts for strategic planning only.")