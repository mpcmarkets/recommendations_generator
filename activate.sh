#!/bin/bash

# Investment Recommendation Generator - Local Development Setup
# Activates virtual environment and provides helpful commands for local development

set -euo pipefail

# Configuration
APP_NAME="Investment Recommendation Generator"
APP_URL="http://localhost:8501"
PYTHON_VERSION="3.11+"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_header() { echo -e "${CYAN}=== $1 ===${NC}"; }

# Main setup function
setup_environment() {
    log_header "$APP_NAME - Local Development Setup"
    
    # Check Python version
    if ! python3 --version | grep -q "Python 3"; then
        log_error "Python 3 is required but not found"
        exit 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv .venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    log_info "Activating virtual environment..."
    source .venv/bin/activate
    
    # Check and install requirements
    if ! python -c "import streamlit" 2>/dev/null; then
        log_info "Installing requirements..."
        pip install --upgrade pip
        pip install -r requirements.txt
        log_success "Requirements installed"
    else
        log_success "Requirements already installed"
    fi
    
    # Check LaTeX availability
    if command -v pdflatex >/dev/null 2>&1; then
        log_success "LaTeX is available - PDF generation enabled"
    else
        log_warning "LaTeX not found - PDF generation will not work"
        log_info "Install LaTeX: sudo apt-get install texlive-latex-base texlive-latex-extra"
    fi
}

# Show available commands
show_commands() {
    echo
    log_header "Available Commands"
    echo "  streamlit run app.py                    # Start the application"
    echo "  streamlit run app.py --server.port 8502 # Start on different port"
    echo "  streamlit run app.py --server.runOnSave true  # Auto-reload on changes"
    echo "  python -c 'import app'                  # Test imports"
    echo "  python -c 'from config import *'        # Test configuration"
    echo "  deactivate                              # Exit virtual environment"
    echo
    log_info "Application will be available at: $APP_URL"
    echo
    log_info "💡 Tip: Run 'streamlit run app.py' to start the application"
}

# Main execution
main() {
    setup_environment
    show_commands
}

# Run main function
main "$@"
