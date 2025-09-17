#!/bin/bash

# Investment Recommendation Generator - Docker Deployment Script
# Provides easy commands for Docker deployment and management
#
# Usage: ./docker-deploy.sh [COMMAND]
# Commands: start, stop, restart, logs, status, cleanup, help

set -euo pipefail

# Configuration
APP_NAME="Investment Recommendation Generator"
APP_URL="http://localhost:8501"
CONTAINER_NAME="investment-recommendation-app"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Utility functions
check_docker() {
    log_info "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log_success "Docker is running"
}

create_directories() {
    log_info "Creating data directories..."
    mkdir -p data/{pdfs,images,logs,temp}
    log_success "Data directories created"
}

wait_for_health() {
    log_info "Waiting for application to be healthy..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "${APP_URL}/_stcore/health" > /dev/null 2>&1; then
            log_success "Application is healthy"
            return 0
        fi
        log_info "Attempt $attempt/$max_attempts - waiting for application..."
        sleep 2
        ((attempt++))
    done
    
    log_warning "Application may not be fully ready yet"
    return 1
}

# Main application functions
start_app() {
    log_header "Starting $APP_NAME"
    check_docker
    create_directories
    
    log_info "Building and starting application..."
    if docker-compose up --build -d; then
        log_success "Application started successfully!"
        wait_for_health
        log_info "Access the application at: $APP_URL"
    else
        log_error "Failed to start application"
        exit 1
    fi
}

stop_app() {
    log_header "Stopping $APP_NAME"
    log_info "Stopping application..."
    if docker-compose down; then
        log_success "Application stopped"
    else
        log_error "Failed to stop application"
        exit 1
    fi
}

restart_app() {
    log_header "Restarting $APP_NAME"
    log_info "Restarting application..."
    if docker-compose restart; then
        log_success "Application restarted"
        wait_for_health
        log_info "Access the application at: $APP_URL"
    else
        log_error "Failed to restart application"
        exit 1
    fi
}

view_logs() {
    log_header "Application Logs"
    log_info "Showing application logs (Press Ctrl+C to exit)..."
    docker-compose logs -f recommendation-app
}

check_status() {
    log_header "Application Status"
    if docker-compose ps | grep -q "Up"; then
        log_success "Application is running"
        log_info "Access at: $APP_URL"
        
        # Check health endpoint
        if curl -f -s "${APP_URL}/_stcore/health" > /dev/null 2>&1; then
            log_success "Application is healthy"
        else
            log_warning "Application is running but may not be fully ready"
        fi
    else
        log_warning "Application is not running"
    fi
}

cleanup() {
    log_header "Cleaning Up Docker Resources"
    log_warning "This will remove all containers, volumes, and unused images"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Stopping and removing containers..."
        docker-compose down -v
        log_info "Cleaning up unused Docker resources..."
        docker system prune -f
        log_success "Cleanup completed"
    else
        log_info "Cleanup cancelled"
    fi
}

# Help function
show_help() {
    cat << EOF
$APP_NAME - Docker Deployment Script

USAGE:
    $0 [COMMAND]

COMMANDS:
    start     Build and start the application
    stop      Stop the application
    restart   Restart the application
    logs      View application logs (follow mode)
    status    Check application status and health
    cleanup   Stop application and clean up Docker resources
    help      Show this help message

EXAMPLES:
    $0 start      # Start the application
    $0 logs       # View live logs
    $0 status     # Check if running
    $0 cleanup    # Clean up everything

ENVIRONMENT:
    Application URL: $APP_URL
    Container Name: $CONTAINER_NAME

EOF
}

# Main script logic
main() {
    case "${1:-help}" in
        start)
            start_app
            ;;
        stop)
            stop_app
            ;;
        restart)
            restart_app
            ;;
        logs)
            view_logs
            ;;
        status)
            check_status
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
