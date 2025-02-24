from kafka import KafkaProducer
import random
import time
import json
from datetime import datetime
import uuid

# Kafka Configuration
KAFKA_BROKER = "localhost:29092"
TOPIC = "logs"

# System Components
COMPONENTS = ["web-server", "database", "auth-service", "api-gateway", "cache-service"]
ENDPOINTS = ["/api/users", "/api/products", "/api/orders", "/api/auth", "/health"]
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]
STATUS_CODES = [200, 201, 400, 401, 403, 404, 500, 503]

# Log Templates
LOG_TEMPLATES = {
    "INFO": [
        "Request processed successfully for {endpoint}",
        "Cache hit for key: {resource_id}",
        "User {user_id} authenticated successfully",
        "Database query completed in {duration}ms",
        "Service health check passed"
    ],
    "WARNING": [
        "High response time ({duration}ms) for {endpoint}",
        "Cache miss for key: {resource_id}",
        "Rate limit warning for IP: {ip_address}",
        "Database connection pool running low",
        "Memory usage above 80%"
    ],
    "ERROR": [
        "Request failed for {endpoint} with status {status_code}",
        "Database query timeout after {duration}ms",
        "Authentication failed for user {user_id}",
        "Invalid payload received from {ip_address}",
        "Service dependency {component} not responding"
    ],
    "CRITICAL": [
        "Service {component} is down",
        "Database connection pool exhausted",
        "Memory usage critical: 95%",
        "Disk space below 5% on {component}",
        "Multiple cascade failures detected"
    ]
}

def generate_resource_id():
    return str(uuid.uuid4())[:8]

def generate_user_id():
    return f"user_{random.randint(1000, 9999)}"

def generate_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_log_entry():
    timestamp = datetime.utcnow().isoformat()
    component = random.choice(COMPONENTS)
    
    # Weight the log levels (70% INFO, 20% WARNING, 9% ERROR, 1% CRITICAL)
    log_level = random.choices(
        ["INFO", "WARNING", "ERROR", "CRITICAL"],
        weights=[70, 20, 9, 1]
    )[0]
    
    # Generate context data
    context = {
        "endpoint": random.choice(ENDPOINTS),
        "resource_id": generate_resource_id(),
        "user_id": generate_user_id(),
        "ip_address": generate_ip(),
        "component": component,
        "duration": random.randint(10, 2000),
        "status_code": random.choice(STATUS_CODES)
    }
    
    # Get random message template and format it with context
    message_template = random.choice(LOG_TEMPLATES[log_level])
    message = message_template.format(**context)
    
    log_entry = {
        "timestamp": timestamp,
        "level": log_level,
        "component": component,
        "message": message,
        "context": context
    }
    
    return json.dumps(log_entry)

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8')
)

# Generate and send logs
try:
    while True:
        log_entry = generate_log_entry()
        producer.send(TOPIC, log_entry)
        print(f"Produced: {log_entry}")
        
        # Random delay between 0.1 and 2 seconds
        time.sleep(random.uniform(0.1, 2))

except KeyboardInterrupt:
    print("\nStopping log producer...")
    producer.close()
