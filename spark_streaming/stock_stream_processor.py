from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, FloatType, IntegerType, StringType

# Define the schema for incoming Kafka JSON messages
schema = StructType() \
    .add("c", FloatType()) \
    .add("h", FloatType()) \
    .add("l", FloatType()) \
    .add("o", FloatType()) \
    .add("pc", FloatType()) \
    .add("t", IntegerType()) \
    .add("timestamp", IntegerType()) \
    .add("symbol", StringType())

# Create Spark session
spark = SparkSession.builder \
    .appName("StockPriceKafkaStream") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stock_prices") \
    .load()

# Parse the JSON messages
json_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write parsed data to CSV in micro-batches
query = json_df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "C:/real-time-stock-streaming/output/stock_prices") \
    .option("checkpointLocation", "C:/real-time-stock-streaming/output/checkpoints") \
    .option("header", True) \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
