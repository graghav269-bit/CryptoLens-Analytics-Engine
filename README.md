# CryptoLens - Cryptocurrency Analytics & Forecasting System

## Overview

CryptoLens is a comprehensive cryptocurrency analytics platform designed to provide real-time market monitoring, advanced data visualization, machine learning-based forecasting, and sentiment analysis.

The platform helps users understand market trends, analyze historical cryptocurrency data, generate future price predictions, and evaluate market sentiment through an interactive dashboard built with Streamlit.

---

## Features

### Live Market Tracking
- Real-time cryptocurrency price monitoring
- Binance API integration
- Bitcoin (BTC), Ethereum (ETH), and Solana (SOL) support
- 24-hour market movement analysis
- Price trend visualization

### Interactive Data Analysis
- Correlation heatmaps
- Distribution histograms
- Volatility analysis
- Trend exploration
- Interactive charts and graphs

### Predictive AI Forecasting
- Facebook Prophet forecasting model
- ARIMA time-series forecasting
- LSTM deep learning forecasting
- Future price prediction
- Model performance evaluation

### Social Sentiment Analysis
- News sentiment analysis
- NLP-based text processing
- Positive, Negative, and Neutral sentiment classification
- Crypto market sentiment monitoring

### Model Comparison
- Compare forecasting models
- Performance metric evaluation
- Accuracy comparison
- Visual model assessment

---

## Technologies Used

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python

### Data Processing
- Pandas
- NumPy

### Data Visualization
- Plotly
- Matplotlib
- Seaborn

### Machine Learning
- Facebook Prophet
- ARIMA
- TensorFlow
- Keras
- Scikit-Learn

### Natural Language Processing
- NLTK
- TextBlob
- VADER Sentiment

### APIs
- Binance API
- News API

---

## System Architecture

Data Collection Layer
        |
        v
Cryptocurrency APIs
        |
        v
Data Processing & Cleaning
        |
        +-----------------------+
        |                       |
        v                       v
EDA Module             Sentiment Module
        |
        v
Forecasting Models
(Prophet, ARIMA, LSTM)
        |
        v
Streamlit Dashboard
        |
        v
User Interface

---

## Project Structure

CryptoLens/

├── app.py

├── pages/
│   ├── Live_Prices.py
│   ├── EDA.py
│   ├── Forecasting.py
│   ├── Sentiment.py
│   └── Model_Comparison.py

├── utils/
│   ├── data_loader.py
│   ├── forecasting.py
│   ├── sentiment.py
│   └── theme.py

├── data/
│   └── crypto_data.csv

├── models/
│   ├── prophet_model.pkl
│   ├── arima_model.pkl
│   └── lstm_model.h5

├── assets/

├── requirements.txt

└── README.md

---

## Installation

1. Clone the repository

git clone https://github.com/yourusername/CryptoLens.git

2. Navigate to the project directory

cd CryptoLens

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

5. Install dependencies

pip install -r requirements.txt

---

## Running the Application

Run the following command:

streamlit run app.py

The application will be available at:

http://localhost:8501

---

## Dashboard Modules

1. Home Dashboard
   - Project overview
   - System introduction
   - Navigation hub

2. Live Prices
   - Real-time cryptocurrency tracking
   - Market statistics
   - Price updates

3. Exploratory Data Analysis (EDA)
   - Historical data analysis
   - Correlation analysis
   - Visual insights

4. Forecasting
   - Prophet predictions
   - ARIMA forecasts
   - LSTM forecasts

5. Sentiment Analysis
   - News sentiment evaluation
   - Market mood assessment
   - NLP-based insights

6. Model Comparison
   - Compare model performance
   - Accuracy analysis
   - Forecast evaluation

---

## Future Enhancements

- Portfolio management system
- Multi-cryptocurrency forecasting
- Advanced deep learning models
- User authentication system
- Cloud deployment
- Trading signal generation
- AI-powered recommendation engine
- Mobile application support

---

## Learning Outcomes

This project demonstrates practical implementation of:

- Data Analytics
- Data Visualization
- Machine Learning
- Deep Learning
- Time Series Forecasting
- Natural Language Processing
- API Integration
- Dashboard Development
- Real-Time Data Processing

---

## Academic Relevance

CryptoLens is developed as an MCA Major Project to showcase the integration of modern data analytics and machine learning techniques in the cryptocurrency domain.

The project combines:
- Real-Time Analytics
- Predictive Modeling
- Artificial Intelligence
- Data Visualization
- NLP Techniques

into a single end-to-end application.

---

## Developer

Raghav Gupta

MCA Student
Aspiring Data Analyst and Machine Learning Enthusiast

Skills:
- Python
- SQL
- Power BI
- Tableau
- Machine Learning
- Data Analytics
- Streamlit

---

## License

This project is developed for educational and academic purposes only.
