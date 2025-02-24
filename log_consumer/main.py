from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand, to_json, struct, expr
import json
from pymongo import MongoClient

# Kafka
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "logs"

# MongoDB
MONGO_URI = "mongodb://root:example@mongodb:27017"
MONGO_DB = "logs_db"
MONGO_COLLECTION = "logs"

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("LogAnomalyDetection") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4") \
    .getOrCreate()

# Read logs from Kafka
log_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .load() \
    .selectExpr("CAST(value AS STRING) as log")

# Parse JSON logs
parsed_logs = log_stream.withColumn("level", expr("get_json_object(log, '$.level')"))

# Define Probabilities for Filtering
PROBABILITIES = {
    "CRITICAL": 0.50,  # 50% chance
    "ERROR": 0.30,     # 30% chance
    "WARNING": 0.15,   # 15% chance
    "INFO": 0.05       # 5% chance
}

# Add a random value column for probabilistic filtering
filtered_logs = parsed_logs.withColumn("random_value", rand()).filter(
    (col("level") == "CRITICAL") & (col("random_value") <= PROBABILITIES["CRITICAL"]) |
    (col("level") == "ERROR") & (col("random_value") <= PROBABILITIES["ERROR"]) |
    (col("level") == "WARNING") & (col("random_value") <= PROBABILITIES["WARNING"]) |
    (col("level") == "INFO") & (col("random_value") <= PROBABILITIES["INFO"])
)

# Very Basic Anomaly Detection
final_logs = filtered_logs.withColumn(
    "status",
    when(col("level").isin("ERROR", "CRITICAL"), "ANOMALY").otherwise("NORMAL")
)

# Write filtered logs to MongoDB
def write_to_mongodb(batch_df, epoch_id):
    print(f"Writing batch {epoch_id} to MongoDB...")

    # Convert DataFrame to JSON
    json_records = batch_df.select(
        to_json(struct("log", "level", "status")).alias("json")
    ).collect()

    print(f"Processing {len(json_records)} records...")
    
    # Prepare for MongoDB insertion
    documents = [json.loads(row.json) for row in json_records]

    if documents:
        collection.insert_many(documents)
        print(f"Inserted {len(documents)} records into MongoDB.")

# Start Streaming Query
query = final_logs.writeStream \
    .foreachBatch(write_to_mongodb) \
    .outputMode("append") \
    .start()

query.awaitTermination()