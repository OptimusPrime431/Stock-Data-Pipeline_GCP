import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import storage
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

today = datetime.now()

# --- Configuration --- #
TICKERS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "TSLA": "Tesla, Inc.",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com, Inc.",
    "NVDA": "NVIDIA Corporation",
    "META": "Meta Platforms, Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "NFLX": "Netflix, Inc.",
    "INTC": "Intel Corporation"
}

START_DATE = (today - timedelta(days=7)).strftime('%Y-%m-%d')
END_DATE = today.strftime('%Y-%m-%d')
LOCAL_FILE = "stocks.json"
LOCAL_PATH = f"/tmp/{LOCAL_FILE}"
GCS_BUCKET_NAME = "stock-bucket8"
GCS_DESTINATION = f"stock_data/date={END_DATE}/{LOCAL_FILE}"

# --- Fetch and combine --- #
all_data = []

for ticker, name in TICKERS.items():
    logging.info(f"Fetching {ticker} from {START_DATE} to {END_DATE}...")
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=START_DATE, end=END_DATE)

        if df.empty:
            logging.warning(f"No data found for {ticker}")
            continue

        df = df.reset_index()
        df['Ticker'] = ticker
        df['Company'] = name
        all_data.append(df)

    except Exception as e:
        logging.error(f"Error fetching {ticker}: {e}")

# --- Combine and save locally --- #
if all_data:
    try:
        result = pd.concat(all_data, ignore_index=True)
        result['Date'] = result['Date'].astype(str)
        result.to_json(LOCAL_PATH, orient='records', lines=True)
        logging.info(f"JSON saved locally at: {LOCAL_PATH}")
    except Exception as e:
        logging.error(f"Error saving JSON locally: {e}")
        raise

    # --- Upload to GCS --- #
    def upload_to_gcs(local_file, bucket_name, gcs_path):
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_file)
            logging.info(f"Uploaded to GCS: gs://{bucket_name}/{gcs_path}")
        except Exception as e:
            logging.error(f"Error uploading to GCS: {e}")
            raise

    upload_to_gcs(LOCAL_PATH, GCS_BUCKET_NAME, GCS_DESTINATION)

else:
    logging.warning( "No stock data was fetched.")
