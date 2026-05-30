import streamlit as st
import pandas as pd
import altair as alt
import requests
import xml.etree.ElementTree as ET
from textblob import TextBlob
from datetime import datetime
from utils.charts import display_image
from utils.data_loader import load_csv
from utils.theme import apply_custom_css

st.set_page_config(page_title="Sentiment Analysis", page_icon="📡", layout="wide")
apply_custom_css()

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
    unsafe_allow_html=True
)

st.markdown("""
<h1>
  <i class="ti ti-antenna-bars-5" style="font-size:2rem; vertical-align:-6px; color:#f472b6;"></i>
  Interactive Market Sentiment Analysis
</h1>
""", unsafe_allow_html=True)

st.markdown("Analyzes price fluctuations and integrates NLP-based sentiment analysis from crypto-related news and social media.")

coins = {"Bitcoin (BTC)": "btc", "Ethereum (ETH)": "eth", "Solana (SOL)": "sol"}
asset_name = st.selectbox("Select Asset to Analyze", list(coins.keys()))
prefix = coins[asset_name]

tabs = st.tabs(["Live NLP Sentiment Pulse", "Historical Analytics Archive"])

# -------- LIVE NLP DASHBOARD --------
with tabs[0]:
    st.markdown(f"""
    <h3>
      <i class="ti ti-broadcast" style="font-size:1.3rem; vertical-align:-3px; color:#f472b6;"></i>
      Real-time Market Sentiment for {asset_name}
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Actively scraping and processing global crypto news feeds using Natural Language Processing.")

    @st.cache_data(ttl=300)
    def fetch_live_news_sentiment(asset_key):
        keyword = asset_key.split()[0].lower()
        url = "https://cointelegraph.com/rss"
        news_list = []
        try:
            r = requests.get(url, timeout=10)
            root = ET.fromstring(r.text)
            items = root.findall('.//item')

            for item in items:
                title_elem = item.find('title')
                desc_elem = item.find('description')
                title = title_elem.text if title_elem is not None and title_elem.text else ""
                desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                pubdate_elem = item.find('pubDate')
                pubdate = pubdate_elem.text if pubdate_elem is not None and pubdate_elem.text else str(datetime.now())

                content = (title + " " + desc).lower()
                if keyword in content or "crypto" in content:
                    blob = TextBlob(title + " " + desc)
                    sentiment = blob.sentiment.polarity

                    if sentiment > 0.05:
                        label = 'Positive'
                    elif sentiment < -0.05:
                        label = 'Negative'
                    else:
                        label = 'Neutral'

                    news_list.append({
                        "Headline": title,
                        "NLP Polarity": round(sentiment, 3),
                        "Classification": label,
                        "Published": pubdate
                    })

            df = pd.DataFrame(news_list)
            if not df.empty:
                df = df.drop_duplicates(subset=['Headline']).sort_values('NLP Polarity', ascending=False)
            return df
        except Exception:
            return pd.DataFrame()

    with st.spinner("Scraping live feeds and streaming to NLP Engine..."):
        live_df = fetch_live_news_sentiment(asset_name)

    if not live_df.empty:
        pos_count = len(live_df[live_df['Classification'] == 'Positive'])
        neg_count = len(live_df[live_df['Classification'] == 'Negative'])
        neu_count = len(live_df[live_df['Classification'] == 'Neutral'])
        avg_polarity = live_df['NLP Polarity'].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average NLP Polarity",
            f"{avg_polarity:.3f}",
            "Positive" if avg_polarity > 0 else "Negative",
            delta_color="normal" if avg_polarity > 0 else "inverse"
        )
        col2.metric("Total Articles Evaluated", f"{len(live_df)}", "Real-Time")

        # Verdict with directional icon
        if pos_count > neg_count:
            verdict_icon, verdict_label, verdict_color = "ti-trending-up", "Bullish", "#4ade80"
        elif neg_count > pos_count:
            verdict_icon, verdict_label, verdict_color = "ti-trending-down", "Bearish", "#f87171"
        else:
            verdict_icon, verdict_label, verdict_color = "ti-minus", "Neutral", "#94a3b8"

        col3.markdown(f"""
        <div style="font-size:13px; color:#94a3b8; margin-bottom:4px;">Live Market Verdict</div>
        <div style="display:flex; align-items:center; gap:6px; font-size:1.4rem; font-weight:500;">
          <i class="ti {verdict_icon}" style="color:{verdict_color};"></i>
          <span style="color:{verdict_color};">{verdict_label}</span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        col_c1, col_c2 = st.columns([1, 2])

        with col_c1:
            st.markdown("""
            <h4>
              <i class="ti ti-chart-donut" style="font-size:1.1rem; vertical-align:-2px; color:#94a3b8;"></i>
              NLP Distribution Vector
            </h4>
            """, unsafe_allow_html=True)
            dist_df = pd.DataFrame({
                "Sentiment": ["Positive", "Negative", "Neutral"],
                "Count": [pos_count, neg_count, neu_count]
            })
            chart_pie = alt.Chart(dist_df).mark_arc(innerRadius=40).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(
                    domain=["Positive", "Negative", "Neutral"],
                    range=["#2ca02c", "#d62728", "#7f7f7f"]
                )),
                tooltip=['Sentiment', 'Count']
            ).properties(height=300)
            st.altair_chart(chart_pie, use_container_width=True)

        with col_c2:
            st.markdown("""
            <h4>
              <i class="ti ti-news" style="font-size:1.1rem; vertical-align:-2px; color:#94a3b8;"></i>
              Live Processed Headlines
            </h4>
            """, unsafe_allow_html=True)
            styled_df = live_df[['Headline', 'Classification', 'NLP Polarity']].head(15)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

    else:
        st.info("No incoming cryptographic news matching your asset over the past hour. Please try again later.")

# -------- HISTORICAL CSV ARCHIVE --------
with tabs[1]:
    @st.cache_data
    def get_merged_data(prefix):
        price_df = load_csv(f"{prefix}_raw.csv")
        sent_df = load_csv(f"{prefix}_sentiment.csv")

        if price_df.empty or sent_df.empty:
            return pd.DataFrame(), None

        price_date = 'Date' if 'Date' in price_df.columns else 'date' if 'date' in price_df.columns else None
        sent_date = 'Date' if 'Date' in sent_df.columns else 'date' if 'date' in sent_df.columns else None

        if price_date and sent_date:
            price_df['date_merge'] = pd.to_datetime(price_df[price_date]).dt.normalize()
            sent_df['date_merge'] = pd.to_datetime(sent_df[sent_date]).dt.normalize()

            merged = pd.merge(price_df, sent_df, on='date_merge', how='inner')
            merged.sort_values('date_merge', inplace=True)

            close_col = 'Close' if 'Close' in merged.columns else 'close' if 'close' in merged.columns else None
            if close_col:
                merged['daily_return'] = merged[close_col].pct_change()
            return merged, close_col
        return pd.DataFrame(), None

    merged_df, close_col = get_merged_data(prefix)

    if not merged_df.empty and close_col:
        st.markdown(f"""
        <h3>
          <i class="ti ti-database" style="font-size:1.3rem; vertical-align:-3px; color:#94a3b8;"></i>
          Daily Sentiment vs Price ({asset_name})
        </h3>
        """, unsafe_allow_html=True)

        base = alt.Chart(merged_df).encode(x=alt.X('date_merge:T', title='Date'))

        line_price = base.mark_line(color='#f7931a').encode(
            y=alt.Y(f'{close_col}:Q', title='Price (USD)', scale=alt.Scale(zero=False))
        )

        sent_col = 'sentiment_smooth' if 'sentiment_smooth' in merged_df.columns else 'sentiment_mean' if 'sentiment_mean' in merged_df.columns else None

        if sent_col:
            line_sent = base.mark_area(color='#5c88da', opacity=0.3).encode(
                y=alt.Y(f'{sent_col}:Q', title='Sentiment Score')
            )
            chart = alt.layer(line_price, line_sent).resolve_scale(y='independent').interactive().properties(height=400)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.line_chart(merged_df.set_index('date_merge')[close_col])

        st.divider()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            <h3>
              <i class="ti ti-chart-scatter" style="font-size:1.2rem; vertical-align:-3px; color:#818cf8;"></i>
              Price Returns vs Sentiment Correlation
            </h3>
            """, unsafe_allow_html=True)
            if sent_col and 'daily_return' in merged_df.columns:
                scatter = alt.Chart(merged_df.dropna(subset=[sent_col, 'daily_return'])).mark_circle(size=60).encode(
                    x=alt.X(f'{sent_col}:Q', title='Sentiment Score'),
                    y=alt.Y('daily_return:Q', title='Daily Return', axis=alt.Axis(format='%')),
                    color=alt.condition(alt.datum.daily_return > 0, alt.value("#2ca02c"), alt.value("#d62728")),
                    tooltip=['date_merge:T', close_col, sent_col, 'daily_return']
                ).interactive().properties(height=350)

                trend = scatter.transform_regression(sent_col, 'daily_return').mark_line(color='white')
                st.altair_chart(scatter + trend, use_container_width=True)

                corr_val = merged_df[sent_col].corr(merged_df['daily_return'])
                st.caption(f"Pearson Correlation Coefficient: **{corr_val:.3f}**")

        with col2:
            st.markdown("""
            <h3>
              <i class="ti ti-chart-donut-3" style="font-size:1.2rem; vertical-align:-3px; color:#f472b6;"></i>
              Aggregate Sentiment Distribution
            </h3>
            """, unsafe_allow_html=True)
            if 'positive_ratio' in merged_df.columns and 'negative_ratio' in merged_df.columns:
                pos = merged_df['positive_ratio'].mean()
                neg = merged_df['negative_ratio'].mean()
                neu = 1.0 - (pos + neg)
                dist_df = pd.DataFrame({
                    "Sentiment": ["Positive", "Negative", "Neutral"],
                    "Ratio": [pos, neg, neu]
                })
                chart_pie = alt.Chart(dist_df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Ratio", type="quantitative"),
                    color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(
                        domain=["Positive", "Negative", "Neutral"],
                        range=["#2ca02c", "#d62728", "#7f7f7f"]
                    )),
                    tooltip=['Sentiment', alt.Tooltip('Ratio:Q', format='.1%')]
                ).properties(height=350)
                st.altair_chart(chart_pie, use_container_width=True)

        st.divider()

        st.markdown("""
        <h3>
          <i class="ti ti-tags" style="font-size:1.2rem; vertical-align:-3px; color:#94a3b8;"></i>
          Most Frequent Market Keywords
        </h3>
        """, unsafe_allow_html=True)
        display_image("wordcloud.png", caption="Wordcloud generated from News & Twitter corpus")

    else:
        st.warning(f"Insufficient historical data available to merge Prices with Sentiment Data for {asset_name}.")