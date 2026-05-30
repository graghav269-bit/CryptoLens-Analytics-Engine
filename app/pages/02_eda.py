import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils.data_loader import get_historical_klines
from utils.theme import apply_custom_css

st.set_page_config(page_title="EDA (Live Data)", page_icon="📊", layout="wide")
apply_custom_css()

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

st.markdown("""
<h1>
  <i class="ti ti-chart-dots" style="font-size:2rem; vertical-align:-6px; color:#38bdf8;"></i>
  Live Exploratory Data Analysis
</h1>
""", unsafe_allow_html=True)

st.markdown("Visualizing real-time historical trends, volume, volatility, and correlations using live Binance API data.")

symbols = {"BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "SOLUSDT": "Solana"}
days = st.slider("Select Time Horizon (Days)", min_value=30, max_value=730, value=365)

@st.cache_data(ttl=3600)
def load_all_data(days):
    dfs = {}
    for sym, name in symbols.items():
        df = get_historical_klines(sym, interval='1d', limit=days)
        if not df.empty:
            df.set_index('Date', inplace=True)
            dfs[name] = df
    return dfs

dfs = load_all_data(days)

if not dfs:
    st.error("Failed to fetch live data from Binance. Please try again later.")
    st.stop()

# 1. Price Overview (Normalized)
st.markdown("""
<h3>
  <i class="ti ti-align-box-left-stretch" style="font-size:1.2rem; vertical-align:-3px; color:#94a3b8;"></i>
  Normalized Price Overview
</h3>
""", unsafe_allow_html=True)
st.markdown("Comparing relative price movements (base index = 100) from the beginning of the selected period.")

price_df = pd.DataFrame({name: df['Close'] for name, df in dfs.items()}).dropna()

if not price_df.empty:
    normalized_prices = (price_df / price_df.iloc[0]) * 100
    st.line_chart(normalized_prices)

# 2. Returns Distribution & Correlation
st.divider()
returns_df = price_df.pct_change().dropna() * 100

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <h3>
      <i class="ti ti-chart-histogram" style="font-size:1.2rem; vertical-align:-3px; color:#fb923c;"></i>
      Daily Returns Distribution
    </h3>
    """, unsafe_allow_html=True)
    melted_returns = returns_df.reset_index().melt(id_vars='Date', var_name='Asset', value_name='Daily Return (%)')
    chart = alt.Chart(melted_returns).mark_bar(opacity=0.7).encode(
        alt.X('Daily Return (%):Q', bin=alt.Bin(maxbins=50)),
        alt.Y('count()', title='Frequency'),
        color='Asset:N'
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.markdown("""
    <h3>
      <i class="ti ti-grid-dots" style="font-size:1.2rem; vertical-align:-3px; color:#818cf8;"></i>
      Returns Correlation Heatmap
    </h3>
    """, unsafe_allow_html=True)
    corr = returns_df.corr().reset_index().melt(id_vars='index')
    corr.columns = ['Asset 1', 'Asset 2', 'Correlation']
    heat = alt.Chart(corr).mark_rect().encode(
        x='Asset 1:O',
        y='Asset 2:O',
        color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='redblue', domain=[-1, 1])),
        tooltip=['Asset 1', 'Asset 2', 'Correlation']
    ).properties(height=300)
    text = heat.mark_text(baseline='middle').encode(
        text=alt.Text('Correlation:Q', format='.2f'),
        color=alt.condition(
            alt.datum.Correlation > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )
    st.altair_chart(heat + text, use_container_width=True)

# 3. Volatility Analysis
st.divider()
st.markdown("""
<h3>
  <i class="ti ti-activity" style="font-size:1.2rem; vertical-align:-3px; color:#f87171;"></i>
  Volatility Analysis (30-Day Rolling Std Dev)
</h3>
""", unsafe_allow_html=True)
st.markdown("Measures the standard deviation of daily returns over a rolling 30-day window.")

volatility_df = returns_df.rolling(window=30).std()
st.line_chart(volatility_df.dropna())

# 4. Volume Over Time
st.divider()
st.markdown("""
<h3>
  <i class="ti ti-chart-bar" style="font-size:1.2rem; vertical-align:-3px; color:#4ade80;"></i>
  Trading Volume Over Time
</h3>
""", unsafe_allow_html=True)

selected_asset_vol = st.selectbox("Select Asset for Volume analysis", list(symbols.values()))
if selected_asset_vol in dfs:
    vol_df = dfs[selected_asset_vol][['Volume']]
    st.bar_chart(vol_df)