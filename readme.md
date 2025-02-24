# Real-Time Log Processing Pipeline with Kafka, Spark, and MongoDB

## Overview
This project implements a **real-time log processing pipeline** using Apache Kafka, Apache Spark, and MongoDB. The system ingests logs from a producer, processes them using Spark Streaming, and selectively stores them in MongoDB based on severity.

## Architecture
The system consists of the following components:

- **Kafka**: A distributed message broker that collects and distributes log messages.
- **Zookeeper**: Manages Kafka brokers and maintains metadata.
- **Spark Streaming**: Processes logs in real-time and applies filtering based on severity.
- **MongoDB**: Stores processed logs for further analysis and retrieval.
- **Mongo-Express**: A web-based admin panel for MongoDB.
- **Log Producer**: Simulates log generation and publishes them to Kafka topics.
- **Log Consumer**: A Spark application that processes Kafka logs and stores relevant logs in MongoDB.

## Components

### 1. Apache Kafka
Kafka acts as the central event streaming platform, collecting and distributing logs from producers to consumers.

### 2. Apache Zookeeper
Zookeeper coordinates Kafka brokers, managing leader election and metadata.

### 3. Apache Spark
Spark Streaming consumes logs from Kafka, classifies them by severity, and stores a subset of logs in MongoDB.

### 4. MongoDB
MongoDB serves as a storage backend for processed logs, allowing for later retrieval and analysis.

### 5. Mongo-Express
Mongo-Express provides a user-friendly web interface for exploring logs stored in MongoDB.

### 6. Log Producer
A Python-based script that generates and sends simulated log messages to Kafka.

### 7. Log Consumer
A Spark application that filters logs based on severity and inserts a percentage of each severity level into MongoDB.

## Deployment with Docker Compose
To deploy the system using Docker Compose, run:

```sh
docker-compose up -d
```

This will start all services, including Kafka, Zookeeper, Spark, MongoDB, and the log processing pipeline.

## Configuration

- Kafka Broker: `kafka:9092`
- MongoDB URI: `mongodb://root:example@mongodb:27017`
- Spark Master: `spark://spark-master:7077`
- Kafka Topic: `logs`

## Log Processing Logic
The log consumer classifies logs into four levels:
- **Critical** (50% chance of being saved)
- **Error** (30% chance)
- **Warning** (15% chance)
- **Info** (5% chance)

This selective persistence reduces storage usage while retaining high-priority logs for analysis.

## Monitoring and Access

- Kafka UI: [Conduktor](https://www.conduktor.io/) or `kafka-console-consumer`
- Spark UI: `http://localhost:8080`
- Mongo-Express: `http://localhost:8081`
- MongoDB CLI: 
  ```sh
  docker exec -it mongodb mongosh -u root -p example
  ```

## Contribution
Feel free to fork this repository, submit issues, or make pull requests to improve the system.

## License
This project is licensed under the MIT License.
