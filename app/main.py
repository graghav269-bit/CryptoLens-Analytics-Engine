import streamlit as st
from utils.theme import apply_custom_css

st.set_page_config(
    page_title="CryptoLens System",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Tabler icons CDN (add this once at the top)
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

# Hero Section — replace 🌌 with a radar/satellite icon
st.markdown("""
<h1 style='text-align: center; font-size: 3.5rem;'>
  <i class="ti ti-radar-2" style="font-size:3rem; vertical-align:-8px;"></i> CryptoLens Analytics Engine
</h1>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 1.25rem; color: #a0aec0; margin-bottom: 3rem;'>Your premier intelligence platform for cryptocurrency market data, predictive ML modeling, and social sentiment tracking.</p>", unsafe_allow_html=True)

st.divider()

st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Core Intelligence Modules</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    # Replace 📈 with ti-trending-up (candlestick chart feel)
    st.markdown("""
    <h3><i class="ti ti-trending-up" style="font-size:1.4rem; vertical-align:-3px; color:#4ade80;"></i> Live Market Tracking</h3>
    """, unsafe_allow_html=True)
    st.info("Monitor real-time spot prices for Bitcoin, Ethereum, and Solana natively from the Binance API. Track 24-hour pricing deltas instantaneously.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Replace 🔮 with ti-brain (ML model feel, not mystical)
    st.markdown("""
    <h3><i class="ti ti-brain" style="font-size:1.4rem; vertical-align:-3px; color:#818cf8;"></i> Predictive AI Forecasting</h3>
    """, unsafe_allow_html=True)
    st.success("Deploy sophisticated Machine Learning models directly in your browser. Dynamically train **Facebook Prophet** and **ARIMA**, and run inference on deep learning **LSTM** models.")

with col2:
    # Replace 📊 with ti-chart-histogram (more specific than bar chart)
    st.markdown("""
    <h3><i class="ti ti-chart-histogram" style="font-size:1.4rem; vertical-align:-3px; color:#fb923c;"></i> Interactive Data Analysis</h3>
    """, unsafe_allow_html=True)
    st.warning("Generate dynamic correlation heatmaps, asset return distribution histograms, and 30-day trailing volatility metrics calculated on-the-fly.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Replace 🧠 with ti-message-dots (social/NLP feel)
    st.markdown("""
    <h3><i class="ti ti-messages" style="font-size:1.4rem; vertical-align:-3px; color:#f87171;"></i> Social Sentiment Processing</h3>
    """, unsafe_allow_html=True)
    st.error("Analyzes price fluctuations and integrates NLP-based sentiment analysis from crypto-related news and social media.")

st.divider()

# Replace 🎯 with ti-layout-dashboard
st.markdown("""
<div style="text-align: center; background-color: #151e2e; padding: 30px; border-radius: 12px; border: 1px solid #1f2a40; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
    <h3 style="margin-top: 0; background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        <i class="ti ti-layout-dashboard" style="font-size:1.3rem; vertical-align:-3px; color:#4facfe; -webkit-text-fill-color: #4facfe;"></i>
        Initialize Dashboard
    </h3>
    <p style="color: #e2e8f0; font-size: 1.15rem; margin-bottom: 0;">Select any of the specialized modules from the left navigation sidebar to begin exploring.</p>
</div>
""", unsafe_allow_html=True)