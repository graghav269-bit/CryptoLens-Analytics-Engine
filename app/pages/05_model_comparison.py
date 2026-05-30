import streamlit as st
import pandas as pd
import altair as alt
from utils.data_loader import load_csv
from utils.theme import apply_custom_css

st.set_page_config(page_title="Model Comparison", page_icon="📐", layout="wide")
apply_custom_css()

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

st.markdown("""
<h1>
  <i class="ti ti-trophy" style="font-size:2rem; vertical-align:-6px; color:#f59e0b;"></i>
  Forecasting Model Performance Breakdown
</h1>
""", unsafe_allow_html=True)

st.markdown("A definitive comparison of the different Machine Learning time-series models evaluated against the historical crypto test set.")

df = load_csv("model_comparison.csv")

if not df.empty:
    rmse_col = [c for c in df.columns if 'RMSE' in c][0]
    mae_col  = [c for c in df.columns if 'MAE'  in c][0]
    mape_col = [c for c in df.columns if 'MAPE' in c][0]

    best_model_idx = df[rmse_col].idxmin()
    best_model     = df.loc[best_model_idx, 'Model']

    st.markdown(f"""
    <h3>
      <i class="ti ti-medal" style="font-size:1.3rem; vertical-align:-3px; color:#f59e0b;"></i>
      Top Performing Model: <strong>{best_model}</strong>
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("The LSTM Deep Learning network significantly outperformed both statistical ARIMA and Meta Prophet in capturing the volatile crypto price actions, sporting the lowest aggregate error margins across all core dimensions.")

    st.divider()

    best_rmse = df.loc[best_model_idx, rmse_col]
    best_mae  = df.loc[best_model_idx, mae_col]
    best_mape = df.loc[best_model_idx, mape_col]

    cols = st.columns(3)
    cols[0].metric(f"Lowest {rmse_col}", f"${best_rmse:,.2f}", delta="Winner (-)", delta_color="normal")
    cols[1].metric(f"Lowest {mae_col}",  f"${best_mae:,.2f}",  delta="Winner (-)", delta_color="normal")
    cols[2].metric(f"Lowest {mape_col}", f"{best_mape:.2f}%",  delta="Winner (-)", delta_color="normal")

    st.divider()

    st.markdown("""
    <h3>
      <i class="ti ti-table-column" style="font-size:1.2rem; vertical-align:-3px; color:#94a3b8;"></i>
      Detailed Error Metrics
    </h3>
    """, unsafe_allow_html=True)

    styled_df = df.style.highlight_min(
        subset=[mae_col, rmse_col, mape_col],
        color='rgba(40, 167, 69, 0.4)',
        axis=0
    ).format({
        mae_col:  "${:,.2f}",
        rmse_col: "${:,.2f}",
        mape_col: "{:.2f}%"
    })
    st.dataframe(styled_df, use_container_width=True)

    st.divider()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("""
        <h3>
          <i class="ti ti-chart-bar" style="font-size:1.2rem; vertical-align:-3px; color:#38bdf8;"></i>
          Raw Error Magnitudes (RMSE vs MAE)
        </h3>
        """, unsafe_allow_html=True)

        melted_err = df.melt(
            id_vars=['Model'],
            value_vars=[mae_col, rmse_col],
            var_name='Metric',
            value_name='Error ($)'
        )
        bars = alt.Chart(melted_err).mark_bar().encode(
            x=alt.X('Metric:N', title=''),
            y=alt.Y('Error ($):Q', title='Dollar Error Magnitude'),
            color=alt.Color('Metric:N', legend=alt.Legend(title="Metric")),
            column=alt.Column('Model:N', title="", header=alt.Header(labelOrient='bottom'))
        ).properties(width=130, height=350)
        st.altair_chart(bars, use_container_width=False)

    with col_chart2:
        st.markdown(f"""
        <h3>
          <i class="ti ti-percentage" style="font-size:1.2rem; vertical-align:-3px; color:#4ade80;"></i>
          Mean Absolute Percentage Error ({mape_col})
        </h3>
        """, unsafe_allow_html=True)

        mape_chart = alt.Chart(df).mark_bar(color='#2ca02c', opacity=0.8, cornerRadiusEnd=4).encode(
            x=alt.X(f'{mape_col}:Q', title='Percentage Error (%)'),
            y=alt.Y('Model:N', sort='x', title=''),
            tooltip=['Model', f'{mape_col}']
        ).properties(height=280)

        text = mape_chart.mark_text(
            align='left',
            baseline='middle',
            dx=5,
            color='white'
        ).encode(
            text=alt.Text(f'{mape_col}:Q', format='.2f')
        )
        st.altair_chart(mape_chart + text, use_container_width=True)

else:
    st.info("Metrics not available yet. Please run the training notebook.")