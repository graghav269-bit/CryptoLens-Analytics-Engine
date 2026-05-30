import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
import os

from utils.charts import display_image
from utils.data_loader import get_historical_klines
from utils.theme import apply_custom_css

try:
    from prophet import Prophet
except ImportError:
    Prophet = None

try:
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:
    ARIMA = None

try:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    from keras.models import load_model
    import tensorflow as tf
except ImportError:
    load_model = None


st.set_page_config(page_title="Forecasting & TA", page_icon="📈", layout="wide")
apply_custom_css()

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

st.markdown("""
<h1>
  <i class="ti ti-time-duration" style="font-size:2rem; vertical-align:-6px; color:#818cf8;"></i>
  Price Forecasting Models
</h1>
""", unsafe_allow_html=True)

st.markdown("Dynamically train and run inference on Time-Series Machine Learning Models (LSTM, Prophet, ARIMA) over real-time Binance data.")

col_t1, col_t2 = st.columns([1, 2])
asset = col_t1.selectbox("Select Target Asset for ML Forecasting", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

with st.spinner(f"Fetching 2-year live market data for {asset}..."):
    df_full = get_historical_klines(asset, interval='1d', limit=730)

if df_full.empty:
    st.error("Failed to load live data.")
    st.stop()

df_full.set_index("Date", inplace=True)
close_prices = df_full[['Close']].copy()

tabs = st.tabs(["Prophet", "ARIMA", "LSTM Models", "Interactive TA"])

# ----------------- PROPHET -----------------
with tabs[0]:
    st.markdown("""
    <h3>
      <i class="ti ti-brand-meta" style="font-size:1.3rem; vertical-align:-3px; color:#0866ff;"></i>
      Meta Prophet Forecasting
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Inferences from a pre-trained Facebook Prophet model.")

    if Prophet is not None:
        future_days = st.slider("Prophet Forecast Horizon (Days)", 7, 180, 30, key='prophet_days')

        if st.button("Load and Run Prophet Forecast"):
            with st.spinner("Loading pre-trained Prophet model..."):
                import json
                from prophet.serialize import model_from_json

                model_path = os.path.join(os.path.dirname(__file__), '../../models/prophet_btc.json')
                with open(model_path, 'r') as fin:
                    m = model_from_json(json.load(fin))

                future   = m.make_future_dataframe(periods=future_days)
                forecast = m.predict(future)

                st.markdown("""
                <h4>
                  <i class="ti ti-route" style="font-size:1.1rem; vertical-align:-2px; color:#94a3b8;"></i>
                  Forecast Trajectory
                </h4>
                """, unsafe_allow_html=True)
                fig1 = m.plot(forecast)
                st.pyplot(fig1)

                with st.expander("Show Components"):
                    fig2 = m.plot_components(forecast)
                    st.pyplot(fig2)
    else:
        st.warning("Prophet not installed.")
        display_image("prophet_forecast.png")


# ----------------- ARIMA -----------------
with tabs[1]:
    st.markdown("""
    <h3>
      <i class="ti ti-wave-sine" style="font-size:1.3rem; vertical-align:-3px; color:#fb923c;"></i>
      ARIMA Forecasting
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Dynamically training ARIMA model.")

    if ARIMA is not None:
        arima_days = st.slider("ARIMA Forecast Horizon (Days)", 7, 60, 14, key='arima_days')

        if st.button("Run ARIMA Model"):
            with st.spinner("Training ARIMA model..."):
                data      = close_prices['Close']
                model     = ARIMA(data, order=(5, 1, 0))
                model_fit = model.fit()
                forecast  = model_fit.forecast(steps=arima_days)

                last_date    = close_prices.index[-1]
                future_dates = [last_date + timedelta(days=i) for i in range(1, arima_days + 1)]

                chart_df    = close_prices.tail(90).copy().rename(columns={'Close': 'Historical'})
                forecast_df = pd.DataFrame({'ARIMA Forecast': forecast}, index=future_dates)
                combined_df = pd.concat([chart_df, forecast_df], axis=1)

                st.markdown(f"""
                <h4>
                  <i class="ti ti-chart-line" style="font-size:1.1rem; vertical-align:-2px; color:#fb923c;"></i>
                  ARIMA Forecast for {asset}
                </h4>
                """, unsafe_allow_html=True)
                st.line_chart(combined_df)
    else:
        st.warning("Statsmodels not installed.")
        display_image("arima_forecast.png")


# ----------------- LSTM -----------------
with tabs[2]:
    st.markdown("""
    <h3>
      <i class="ti ti-circuit-cell" style="font-size:1.3rem; vertical-align:-3px; color:#34d399;"></i>
      Deep Learning (LSTM)
    </h3>
    """, unsafe_allow_html=True)

    if load_model is not None:
        if st.button("Load Keras LSTM & Predict"):
            with st.spinner("Loading model..."):
                try:
                    lstm        = load_model("models/lstm_btc.keras")
                    recent_data = close_prices['Close'].tail(60).values

                    min_val     = np.min(recent_data)
                    max_val     = np.max(recent_data)
                    scaled_data = (recent_data - min_val) / (max_val - min_val + 1e-8)

                    x_input    = scaled_data.reshape((1, 60, 1))
                    pred_scaled = lstm.predict(x_input, verbose=0)[0][0]
                    pred_price  = pred_scaled * (max_val - min_val) + min_val

                    st.success("LSTM Prediction successful!")
                    st.metric("Predicted Price", f"${pred_price:.2f}")

                except Exception as e:
                    st.error(f"LSTM Error: {e}")
    else:
        st.warning("TensorFlow not installed.")
        display_image("lstm_forecast.png")


# ----------------- TA -----------------
with tabs[3]:
    st.markdown("""
    <h3>
      <i class="ti ti-chart-candle" style="font-size:1.3rem; vertical-align:-3px; color:#f59e0b;"></i>
      Technical Analysis
    </h3>
    """, unsafe_allow_html=True)

    window  = st.slider("Moving Average Window", 5, 200, 20)
    std_dev = st.slider("Bollinger Std Dev", 1.0, 3.0, 2.0)

    df_ta           = df_full.copy()
    df_ta['SMA']      = df_ta['Close'].rolling(window).mean()
    df_ta['BB_Upper'] = df_ta['SMA'] + df_ta['Close'].rolling(window).std() * std_dev
    df_ta['BB_Lower'] = df_ta['SMA'] - df_ta['Close'].rolling(window).std() * std_dev

    st.markdown("""
    <h4>
      <i class="ti ti-arrows-vertical" style="font-size:1.1rem; vertical-align:-2px; color:#94a3b8;"></i>
      Bollinger Bands & Moving Average
    </h4>
    """, unsafe_allow_html=True)
    st.line_chart(df_ta[['Close', 'SMA', 'BB_Upper', 'BB_Lower']].dropna().tail(365))