from pyspark.sql import SparkSession
from pyspark.sql.functions import window, sum

# Set up Spark session
spark = SparkSession.builder.appName("NetworkTrafficAnalysis").getOrCreate()

# Read data from the Kafka topic using Structured Streaming
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "network-traffic") \
    .load()

# Convert the binary value column to string and split into individual columns
df = df.selectExpr("CAST(value AS STRING)") \
    .selectExpr("split(value, ',')[0] AS source_ip",
                "split(value, ',')[1] AS destination_ip",
                "CAST(split(value, ',')[2] AS INTEGER) AS bytes_sent")

# Perform real-time analytics using stateless transformations
processed_df = df \
    .select("source_ip", "bytes_sent") \
    .groupBy("source_ip") \
    .agg(sum("bytes_sent").alias("total_bytes_sent"))

# Implement sliding window operations and window-based aggregations
windowed_df = processed_df \
    .withWatermark("timestamp", "30 seconds") \
    .groupBy(window("timestamp", "30 seconds", "10 seconds"), "source_ip") \
    .agg(sum("total_bytes_sent").alias("windowed_bytes_sent"))

# Write the processed data to the processed-data Kafka topic
query = windowed_df \
    .selectExpr("CAST(window.start AS STRING)", "CAST(window.end AS STRING)", "source_ip", "windowed_bytes_sent") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("topic", "processed-data") \
    .outputMode("update") \
    .start()

