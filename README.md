# 📈 Automated Stock Market Data Pipeline with Google Cloud Platform

A robust, production-grade ETL pipeline designed to extract, process, and analyze stock market data using Google Cloud technologies. This solution supports a one-time **8-year backfill** and automated **weekly updates** through Cloud Composer (Airflow), Apache Spark (Dataproc), and BigQuery.

---

## 🚀 Project Overview

This project streamlines the end-to-end pipeline for stock data processing:

- 🗂️ **Historical Backfill**: Ingests 8 years of stock data using `yfinance` and processes it via PySpark
- 🔁 **Weekly Incremental Updates**: Fetches and processes fresh stock data every **Wednesday at 1 PM EST**
- ⚙️ **Cloud-Native Orchestration**: Managed with Airflow (Cloud Composer) and executed on Dataproc
- 🧠 **Feature-Rich Outputs**: Adds engineered features like % change, volatility, sentiment, and more
- 📊 **Analytics-Ready**: Output stored in partitioned BigQuery tables and ready for BI dashboards

---

## ⚙️ Tech Stack

| Component         | Technology                        |
|------------------|------------------------------------|
| Orchestration     | Cloud Composer (Apache Airflow)   |
| Data Processing   | Dataproc (Apache Spark)           |
| Storage           | Google Cloud Storage (GCS)        |
| Data Warehouse    | BigQuery (Partitioned Tables)     |
| Visualization     | Tableau / Looker Studio           |
| Data Extraction   | Python + yfinance                 |

---

## 📦 Key Features

✅ Ingests and transforms **8 years** of historical data  
🔄 Schedules weekly data ingestion with **partition-aware writes**  
🧮 Feature Engineering:  
&nbsp;&nbsp;&nbsp;&nbsp;• Daily & percentage price change  
&nbsp;&nbsp;&nbsp;&nbsp;• Volatility and sentiment classification  
&nbsp;&nbsp;&nbsp;&nbsp;• Day/Week/Month breakdowns  
📁 Writes data to structured **GCS folders** and **BigQuery partitions**  
🔗 Ready to power dashboards with real-time filtering and insights

---

## 📊 Sample Stocks (Tickers)

- AAPL – Apple Inc.  
- MSFT – Microsoft Corporation  
- TSLA – Tesla, Inc.  
- GOOGL – Alphabet Inc.  
- AMZN – Amazon.com, Inc.  
- NVDA – NVIDIA Corporation  
- META – Meta Platforms, Inc.  
- JPM – JPMorgan Chase & Co.  
- NFLX – Netflix, Inc.  
- INTC – Intel Corporation  

---

## 📅 Scheduling

| Task            | Frequency         | Schedule (UTC)         |
|-----------------|-------------------|-------------------------|
| Initial Load    | One-time (manual) | N/A                     |
| Weekly Update   | Every Wednesday   | `0 13 * * 3` (1 PM EST) |

> ✨ DAG is configured with `start_date=datetime(2025, 4, 2, 13, 0)` to ensure it begins on a Wednesday.

---

## 🚀 Setup Instructions

### 🔹 Backfill (One-Time)
1. Run `fetch_backfill.py` to fetch 8 years of data using yfinance.
2. Run `spark_backfill.py` on Dataproc to transform and save results to:
3. Load transformed data to BigQuery using `WRITE_TRUNCATE`.

### 🔹 Weekly Updates (Automated)
1. Upload `fetch_weekly.py` and `spark_weekly.py` to GCS.
2. Deploy `dag.py` to Cloud Composer.
3. DAG runs every Wednesday at 1 PM EST:
- Fetches past 7 days
- Uploads JSON to `stock_data/`
- Transforms and writes Parquet to `stock_transformed/`
- Loads to BigQuery with `WRITE_APPEND`

---

## 📜 License

This project is intended for **educational and personal use**. Contributions and forks are welcome!

---

## 🙌 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for free stock data via `yfinance`
- [Google Cloud](https://cloud.google.com/) for cloud-native infrastructure
- [Apache Airflow](https://airflow.apache.org/) for orchestrating modern data workflows

---

📫 Feel free to fork this repo or reach out on [LinkedIn](https://linkedin.com/) to collaborate or share feedback.



