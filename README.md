# 📈 Automated Stock Market Data Pipeline with GCP

A scalable, production-ready ETL pipeline designed to extract, process, and analyze stock market data using Google Cloud Platform. The system automates an initial 8-year historical data load and performs weekly incremental updates using Cloud Composer, PySpark (Dataproc), and BigQuery. Data is enriched with analytical metrics and visualized through dynamic dashboards in Looker Studio.

---

## 🚀 Project Overview

This project automates the complete lifecycle of stock data ingestion:
- 🗂️ **Initial Load**: 8 years of historical stock data ingested and transformed
- 🔁 **Weekly Updates**: New data fetched every week and appended
- ⚙️ **Cloud-Native Workflow**: Orchestrated with Cloud Composer & Dataproc
- 📊 **Visual Insights**: Presented through Looker Studio dashboards

---

## ⚙️ Tech Stack

| Component        | Tool/Service                      |
|------------------|------------------------------------|
| **Orchestration**| Cloud Composer (Apache Airflow)    |
| **Data Processing** | Dataproc (PySpark)              |
| **Storage**      | Google Cloud Storage (GCS)         |
| **Data Warehouse** | BigQuery (partitioned by date)  |
| **Dashboarding** | Looker Studio (formerly Data Studio) |
| **Extraction**   | Python + yfinance                  |

---

## 📦 Features

- ✅ **Initial 8-year data load** into BigQuery (WRITE_TRUNCATE)
- 🔄 **Weekly incremental updates** using partition overwrite (WRITE_APPEND)
- 🧮 Feature engineering: daily change, % change, volatility, sentiment, etc.
- 📆 Partitioned BigQuery table for optimized queries
- 📊 Looker dashboard with company-wise filtering, volatility trends & more

---

## 🧪 Example Tickers
- Apple Inc. (AAPL)
- Microsoft Corporation (MSFT)
- Tesla, Inc. (TSLA)
- Alphabet Inc. (GOOGL)
- Amazon.com, Inc. (AMZN)
- And others...

---

## 🛠 Setup

### 🔹 One-Time Historical Load
1. Run extraction script for 8 years of data using `yfinance`
2. Transform with PySpark
3. Load into BigQuery using `WRITE_TRUNCATE`

### 🔹 Weekly Incremental Loads
- Cloud Composer runs every **Thursday at 1 PM UTC**
- Fetches only the last 7 days of data
- Uploads to GCS in `date=YYYY-MM-DD/` folder
- Transformed data is **appended** to BigQuery table

---

## 📊 Dashboard

- Built using **Looker Studio**
- Connected directly to BigQuery
- Shows:
  - Time series of stock prices
  - Market sentiment (Uptrend, Downtrend, Stable)
  - Volatility distribution
  - Daily averages and comparisons

> 🔗 [Live dashboard link – coming soon]

---

## 📅 Scheduling

| Task               | Frequency     | Schedule (UTC)     |
|--------------------|---------------|---------------------|
| Initial load       | One-time      | Manual              |
| Weekly update      | Every Thursday| `0 13 * * 4`        |

---

## 🎯 Future Enhancements

- Add technical indicators (e.g., RSI, MACD)
- Alert system for unusual market activity
- Integrate real-time data streaming
- Slack/Email alert on DAG failure

---

## 📜 License

This project is intended for educational and personal use. Feel free to fork, contribute, or build upon it.

---

## 🙌 Acknowledgments

- Yahoo Finance for free stock data via `yfinance`
- Google Cloud Platform for an amazing cloud ecosystem



