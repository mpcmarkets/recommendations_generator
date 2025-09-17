#!/bin/bash

# Universal startup script for recommendation generator
# Works with both Docker Compose and Render
set -e

echo "Starting Recommendation Generator..."

# Determine port to use
# Render provides PORT environment variable
# Docker Compose uses STREAMLIT_SERVER_PORT
if [ -n "$PORT" ]; then
    # Render deployment
    STREAMLIT_PORT=$PORT
    echo "Running on Render with port $PORT"
else
    # Docker Compose or local deployment
    STREAMLIT_PORT=${STREAMLIT_SERVER_PORT:-8501}
    echo "Running locally with port $STREAMLIT_PORT"
fi

# Create necessary directories
mkdir -p data/{logs,images,pdfs,temp}

# Set proper permissions
chmod -R 755 data/

echo "Starting Streamlit application on port $STREAMLIT_PORT..."

# Start the application
exec streamlit run app.py \
    --server.port=$STREAMLIT_PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
