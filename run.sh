#!/bin/bash

# Investment Recommendation Generator - Simple Run Script
# Quick script to run the application without virtual environment setup

set -euo pipefail

# Configuration
APP_NAME="Investment Recommendation Generator"
APP_URL="http://localhost:8501"
APP_PORT="8501"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check if streamlit is installed
    if ! command -v streamlit >/dev/null 2>&1; then
        log_warning "Streamlit not found. Installing dependencies..."
        pip install -r requirements.txt
        log_success "Dependencies installed"
    else
        log_success "Streamlit is available"
    fi
    
    # Check LaTeX availability
    if ! command -v pdflatex >/dev/null 2>&1; then
        log_warning "LaTeX (pdflatex) not found. PDF generation will not work."
        log_info "Install LaTeX: sudo apt-get install texlive-latex-base texlive-latex-extra"
    else
        log_success "LaTeX is available - PDF generation enabled"
    fi
}

# Create data directories
create_directories() {
    log_info "Creating data directories..."
    mkdir -p data/{pdfs,images,logs,temp}
    log_success "Data directories created"
}

# Run the application
run_app() {
    log_info "Starting $APP_NAME..."
    log_info "Application will be available at: $APP_URL"
    log_info "Press Ctrl+C to stop the application"
    echo
    
    streamlit run app.py --server.port "$APP_PORT" --server.address 0.0.0.0
}

# Main execution
main() {
    echo "🚀 $APP_NAME - Quick Start"
    echo "=========================="
    echo
    
    check_dependencies
    create_directories
    run_app
}

# Run main function
main "$@"
