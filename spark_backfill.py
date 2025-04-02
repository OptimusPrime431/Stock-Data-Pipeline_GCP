from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, round, when, to_date, year, month, dayofmonth, dayofweek, date_format
)
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session(app_name="stock_json"):
    return SparkSession.builder.appName(app_name).getOrCreate()

def read_data(spark, input_path):
    logger.info(f"Reading data from {input_path}")
    return spark.read.json(input_path, multiLine=False)

def clean_data(df):
    return df.dropna().dropDuplicates()

def transform_data(df):
    df = df.withColumnRenamed("Company", "company") \
           .withColumnRenamed("Ticker", "ticker") \
           .withColumnRenamed("Open", "open") \
           .withColumnRenamed("Close", "close") \
           .withColumnRenamed("High", "high") \
           .withColumnRenamed("Low", "low") \
           .withColumnRenamed("Volume", "volume")

    df = df.withColumn("Date", to_date("Date"))

    df = df.withColumn("year_val", year("Date")) \
           .withColumn("month_val", month("Date")) \
           .withColumn("day_val", dayofmonth("Date")) \
           .withColumn("dayofweek_val", dayofweek("Date")) \
           .withColumn("date_formatted", date_format("Date", "yyyy-MM-dd")) \
           .drop("Dividends", "Stock Splits", "Date")

    df = df.withColumn("open", round("open", 4)) \
           .withColumn("high", round("high", 4)) \
           .withColumn("low", round("low", 4)) \
           .withColumn("close", round("close", 4))

    df = df.withColumn("daily_change", round(col("close") - col("open"), 2)) \
           .withColumn("pct_change", round(((col("close") - col("open")) / col("open")) * 100, 2)) \
           .withColumn("volatility", round(col("high") - col("low"), 2)) \
           .withColumn("is_positive", when(col("close") > col("open"), 1).otherwise(0)) \
           .withColumn("daily_avg", round((col("high") + col("low")) / 2, 2)) \
           .withColumn("range_category", when(col("volatility") < 1, "low")
                                         .when(col("volatility") < 2, "medium")
                                         .otherwise("high")) \
           .withColumn("market_sentiment", 
               when(col("pct_change") > 1, "uptrend")
              .when(col("pct_change") < -1, "downtrend")
              .otherwise("stable"))
    return df

def write_data(df, output_path):
    logger.info(f"Writing transformed data to {output_path}")
    df.write.mode("overwrite").parquet(output_path)

def main():
    spark = create_spark_session()

    today_date = datetime.now().strftime('%Y-%m-%d')
    last_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    input_path = f"gs://stock-bucket5/stock_data/date={last_date}/*.json"
    output_path = f"gs://stock-bucket5/stock_transformed/date={today_date}/"

    df_raw = read_data(spark, input_path)
    df_clean = clean_data(df_raw)
    df_transformed = transform_data(df_clean)
    write_data(df_transformed, output_path)

    spark.stop()
    logger.info("Spark job completed successfully.")

if __name__ == "__main__":
    main()