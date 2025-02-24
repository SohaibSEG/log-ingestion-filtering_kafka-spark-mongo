FROM python:3.9-slim

# Install OpenJDK 17
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Set Java home
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the consumer script
COPY main.py .

# Create checkpoint directory
RUN mkdir -p /tmp/checkpoints

# Command to run the script
CMD ["python", "main.py"]