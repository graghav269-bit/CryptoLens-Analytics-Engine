# live_prices.py
import streamlit as st
import pandas as pd
import requests
from utils.data_loader import load_csv
from utils.theme import apply_custom_css

st.set_page_config(page_title="Live Prices", page_icon="📈", layout="wide")
apply_custom_css()

# Load Tabler Icons
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

# Title — replace 📈 with ti-chart-candle (candlestick = trading/live prices)
st.markdown("""
<h1>
  <i class="ti ti-chart-candle" style="font-size:2rem; vertical-align:-6px; color:#4ade80;"></i>
  Live Crypto Prices
</h1>
""", unsafe_allow_html=True)

st.markdown("View real-time cryptocurrency prices and 24h changes from Binance, alongside historical data.")

coins = {
    "Bitcoin (BTC)":  {"file": "btc_raw.csv", "symbol": "BTCUSDT"},
    "Ethereum (ETH)": {"file": "eth_raw.csv", "symbol": "ETHUSDT"},
    "Solana (SOL)":   {"file": "sol_raw.csv", "symbol": "SOLUSDT"},
}

# Coin-specific icons and accent colors — each visually distinct
COIN_ICONS = {
    "Bitcoin (BTC)":  ("ti-currency-bitcoin", "#f59e0b"),   # amber — BTC orange feel
    "Ethereum (ETH)": ("ti-diamond",          "#818cf8"),   # indigo — ETH brand color
    "Solana (SOL)":   ("ti-bolt",             "#34d399"),   # green — SOL speed/energy
}

@st.cache_data(ttl=60)
def get_live_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return float(data['lastPrice']), float(data['priceChange']), float(data['priceChangePercent'])
    except Exception:
        pass
    return None, None, None

cols = st.columns(3)
dfs = {}

for idx, (name, info) in enumerate(coins.items()):
    df = load_csv(info["file"])
    if not df.empty:
        dfs[name] = df

    live_price, live_change, live_perc = get_live_price(info["symbol"])
    icon_class, icon_color = COIN_ICONS[name]

    # Inject a small branded icon above each metric card
    cols[idx].markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <i class="ti {icon_class}" style="font-size:20px; color:{icon_color};"></i>
            <span style="font-size:13px; color:#a0aec0; font-weight:500;">{name}</span>
        </div>
    """, unsafe_allow_html=True)

    if live_price is not None:
        cols[idx].metric(
            label="Live Price",
            value=f"${live_price:,.2f}",
            delta=f"${live_change:,.2f} ({live_perc:.2f}%)"
        )
    else:
        if name in dfs:
            close_col = 'Close' if 'Close' in dfs[name].columns else 'close' if 'close' in dfs[name].columns else None
            if close_col and len(dfs[name]) > 1:
                latest = dfs[name].iloc[-1][close_col]
                prev   = dfs[name].iloc[-2][close_col]
                diff   = latest - prev
                perc   = (diff / prev) * 100
                cols[idx].metric(
                    label="Archived Price",
                    value=f"${latest:,.2f}",
                    delta=f"${diff:,.2f} ({perc:.2f}%)"
                )

st.divider()

# Replace plain selectbox label with an icon header
st.markdown("""
<h3 style="margin-bottom:0.5rem;">
  <i class="ti ti-history" style="font-size:1.3rem; vertical-align:-3px; color:#94a3b8;"></i>
  Historical Data
</h3>
""", unsafe_allow_html=True)

coin_select = st.selectbox("Select asset:", list(coins.keys()))

if coin_select in dfs:
    df = dfs[coin_select]
    icon_class, icon_color = COIN_ICONS[coin_select]

    st.markdown(f"""
    <h4>
      <i class="ti {icon_class}" style="font-size:1.2rem; vertical-align:-3px; color:{icon_color};"></i>
      {coin_select} Price History
    </h4>
    """, unsafe_allow_html=True)

    close_col = 'Close' if 'Close' in df.columns else 'close' if 'close' in df.columns else None
    date_col  = 'Date'  if 'Date'  in df.columns else 'date'  if 'date'  in df.columns else None

    if close_col and date_col:
        chart_df = df[[date_col, close_col]].set_index(date_col)
        st.line_chart(chart_df)

    # Table section header
    st.markdown("""
    <h4>
      <i class="ti ti-table" style="font-size:1.2rem; vertical-align:-3px; color:#94a3b8;"></i>
      Recent Records
    </h4>
    """, unsafe_allow_html=True)
    st.dataframe(df.tail(10), use_container_width=True)

else:
    st.info("Loading historical data or data not available.")