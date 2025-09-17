#!/bin/bash

# Render startup script for recommendation generator
set -e

echo "Starting Recommendation Generator on Render..."

# Set default port if not provided
export PORT=${PORT:-10000}

# Create necessary directories
mkdir -p data/{logs,images,pdfs,temp}

# Set proper permissions
chmod -R 755 data/

echo "Starting Streamlit application on port $PORT..."

# Start the application
exec streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
