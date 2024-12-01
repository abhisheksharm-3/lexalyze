# Dockerfile
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
ENV HF_HOME="/tmp/lexalyze-cache"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt python-multipart
RUN mkdir -m 777 /tmp/lexalyze-cache
RUN chmod 777 /app
RUN mkdir -m 777 /nltk_data

# Copy the application code
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]