# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for LaTeX, git, and other tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-xetex \
    texlive-luatex \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy ai_tools wheel file and install it
COPY libs/ai_tools-1.0.0-py3-none-any.whl /tmp/
RUN pip install --no-cache-dir /tmp/ai_tools-1.0.0-py3-none-any.whl

# Copy requirements and install other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/{logs,images,pdfs,temp}

# Copy and make startup script executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose port (Render will set the actual port via environment variable)
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/_stcore/health || exit 1

# Run the application using startup script
CMD ["/app/start.sh"]
