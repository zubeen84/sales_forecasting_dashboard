import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_excel("superstore.xls")
    df.columns = df.columns.str.strip()
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

st.title("📈 Sales Forecasting Dashboard")
st.write("Interactive sales forecasting across product categories using Facebook Prophet.")
st.info("Designed for business analysts and strategic planners. Use forecasts to guide inventory and procurement decisions.")
st.divider()

with st.sidebar:
    st.header("📊 Dashboard Settings")
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
    st.subheader("📋 Category Insights")

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

    info = insights[category]
    st.write(f"**Pattern:** {info['pattern']}")
    st.write(f"**Recommendation:** {info['recommendation']}")
    st.write(f"**Risk Level:** {info['risk']}")

    st.divider()
    st.subheader("🏛️ ISO 42001 Governance")
    st.write("✅ **Transparency** - forecast method and uncertainty bands visible")
    st.write("✅ **Accountability** - clear authorship and data source stated")
    st.write("✅ **Limitations** - forecast confidence decreases over longer horizons")
    st.divider()
    st.warning("⚠️ Forecasts are for planning purposes only. Always combine with domain expertise and market knowledge.")
    st.divider()
    st.write("Built by **Zubeen Khalid**")
    st.write("MSc Applied Data Science")

cat_df = df[df["Category"] == category].copy()
monthly = cat_df.groupby(
    pd.Grouper(key="Order Date", freq="M")
)["Sales"].sum().reset_index()
monthly.columns = ["ds", "y"]
monthly = monthly[monthly["y"] > 0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"£{monthly['y'].sum():,.0f}"
    )
with col2:
    st.metric(
        "Avg Monthly Sales",
        f"£{monthly['y'].mean():,.0f}"
    )
with col3:
    st.metric(
        "Peak Month Sales",
        f"£{monthly['y'].max():,.0f}"
    )

st.divider()

if st.button("Generate Forecast", type="primary"):

    with st.spinner("Running Prophet model - please wait..."):

        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            interval_width=0.95
        )
        model.fit(monthly)

        future = model.make_future_dataframe(
            periods=horizon,
            freq="M"
        )
        forecast = model.predict(future)

    st.subheader(f"📈 {category} — {horizon} Month Forecast")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["ds"],
        y=monthly["y"],
        mode="lines+markers",
        name="Actual Sales",
        line=dict(color="#00C9A7", width=2),
        marker=dict(size=4)
    ))

    forecast_only = forecast[forecast["ds"] > monthly["ds"].max()]

    fig.add_trace(go.Scatter(
        x=forecast_only["ds"],
        y=forecast_only["yhat"],
        mode="lines",
        name="Forecast",
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
        name="Confidence Interval",
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

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("📊 Forecast Summary")

    col4, col5, col6 = st.columns(3)

    last_actual = monthly["y"].iloc[-1]
    next_month_forecast = forecast_only["yhat"].iloc[0]
    end_forecast = forecast_only["yhat"].iloc[-1]

    with col4:
        st.metric(
            "Last Actual Month",
            f"£{last_actual:,.0f}"
        )
    with col5:
        change = next_month_forecast - last_actual
        st.metric(
            "Next Month Forecast",
            f"£{next_month_forecast:,.0f}",
            delta=f"£{change:,.0f}"
        )
    with col6:
        st.metric(
            f"Month {horizon} Forecast",
            f"£{end_forecast:,.0f}"
        )

    st.divider()
    st.subheader("💼 Business Recommendation")
    st.success(f"**{category}:** {insights[category]['recommendation']}")
    st.write(f"**Demand Pattern:** {insights[category]['pattern']}")
    st.write(f"**Planning Risk:** {insights[category]['risk']}")
    st.write("**Note:** Confidence intervals widen over longer horizons. Use 6–12 month forecasts for operational decisions and 24–36 month forecasts for strategic planning only.")