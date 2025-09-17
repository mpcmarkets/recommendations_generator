#!/bin/bash

# Investment Recommendation Generator - Unified Deployment Script
# Handles local development, Docker deployment, and environment setup

set -euo pipefail

# Configuration
APP_NAME="Investment Recommendation Generator"
APP_URL="http://localhost:8501"
CONTAINER_NAME="recommendation-app"
IMAGE_NAME="recommendation-generator"
PORT="8501"
DATA_DIR="$(pwd)/data"

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

# Show usage
show_usage() {
    echo -e "${BLUE}$APP_NAME - Deployment Script${NC}"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  local       - Set up local development environment"
    echo "  run         - Run application locally (quick start)"
    echo "  docker      - Deploy with Docker (recommended)"
    echo "  stop        - Stop Docker container"
    echo "  restart     - Restart Docker container"
    echo "  logs        - View Docker logs"
    echo "  status      - Check Docker container status"
    echo "  cleanup     - Clean up Docker resources"
    echo "  help        - Show this help message"
    echo
    echo "Examples:"
    echo "  $0 local     # Set up virtual environment and install dependencies"
    echo "  $0 run       # Quick start without virtual environment"
    echo "  $0 docker    # Deploy with Docker (recommended for production)"
    echo "  $0 logs      # View application logs"
}

# Local development setup
setup_local() {
    log_header "Setting up local development environment"
    
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
    
    # Install requirements
    log_info "Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Requirements installed"
    
    # Check LaTeX availability
    if command -v pdflatex >/dev/null 2>&1; then
        log_success "LaTeX is available - PDF generation enabled"
    else
        log_warning "LaTeX not found - PDF generation will not work"
        log_info "Install LaTeX: sudo apt-get install texlive-latex-base texlive-latex-extra"
    fi
    
    # Create data directories
    log_info "Creating data directories..."
    mkdir -p data/{pdfs,images,logs,temp}
    log_success "Data directories created"
    
    echo
    log_success "Local development environment ready!"
    log_info "Run 'source .venv/bin/activate && streamlit run app.py' to start"
}

# Quick run without virtual environment
run_local() {
    log_header "Quick Start - Running locally"
    
    # Check dependencies
    if ! command -v streamlit >/dev/null 2>&1; then
        log_warning "Streamlit not found. Installing dependencies..."
        pip install -r requirements.txt
        log_success "Dependencies installed"
    fi
    
    # Create data directories
    mkdir -p data/{pdfs,images,logs,temp}
    
    # Check LaTeX
    if ! command -v pdflatex >/dev/null 2>&1; then
        log_warning "LaTeX not found - PDF generation will not work"
    fi
    
    log_info "Starting $APP_NAME..."
    log_info "Application will be available at: $APP_URL"
    log_info "Press Ctrl+C to stop"
    echo
    
    streamlit run app.py --server.port "$PORT" --server.address 0.0.0.0
}

# Docker deployment
deploy_docker() {
    log_header "Docker Deployment"
    
    # Check Docker
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker daemon."
        exit 1
    fi
    
    # Create data directories
    log_info "Creating data directories..."
    mkdir -p "$DATA_DIR"/{logs,images,pdfs,temp}
    log_success "Data directories created"
    
    # Build Docker image
    log_info "Building Docker image..."
    docker build -t "$IMAGE_NAME" .
    log_success "Docker image built successfully"
    
    # Start container
    log_info "Starting application..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$PORT:$PORT" \
        -v "$DATA_DIR:/app/data" \
        --health-cmd="curl -f http://localhost:$PORT || exit 1" \
        --health-interval=10s \
        --health-timeout=5s \
        --health-retries=5 \
        "$IMAGE_NAME" \
        streamlit run app.py --server.port "$PORT" --server.address 0.0.0.0 --server.headless true
    
    log_success "Application started successfully"
    log_info "Container status:"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    log_success "Application is running at: $APP_URL"
    log_info "To view logs: $0 logs"
    log_info "To stop: $0 stop"
}

# Stop Docker container
stop_docker() {
    log_info "Stopping application..."
    if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
        log_success "Application stopped"
    else
        log_info "Application is not running."
    fi
}

# Restart Docker container
restart_docker() {
    stop_docker
    deploy_docker
}

# View Docker logs
view_logs() {
    log_info "Viewing application logs..."
    docker logs -f "$CONTAINER_NAME"
}

# Check Docker status
check_status() {
    log_info "Container status:"
    if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        log_success "Application is running at: $APP_URL"
    else
        log_error "Application is not running."
    fi
}

# Clean up Docker resources
cleanup_docker() {
    log_info "Cleaning up Docker resources..."
    stop_docker
    docker rmi "$IMAGE_NAME" || true
    docker system prune -f
    log_success "Docker resources cleaned up"
}

# Main execution
main() {
    case "${1:-help}" in
        local)
            setup_local
            ;;
        run)
            run_local
            ;;
        docker)
            deploy_docker
            ;;
        stop)
            stop_docker
            ;;
        restart)
            restart_docker
            ;;
        logs)
            view_logs
            ;;
        status)
            check_status
            ;;
        cleanup)
            cleanup_docker
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
