#!/bin/bash

# Docker Run Script for Recommendation Generator
# This script replaces docker-compose for better compatibility

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="recommendation-generator"
CONTAINER_NAME="recommendation-app"
PORT="8501"
DATA_DIR="$(pwd)/data"

# Helper functions
print_header() {
    echo -e "${BLUE}=== Investment Recommendation Generator ===${NC}"
}

print_status() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker status..."
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Create data directories
create_directories() {
    print_status "Creating data directories..."
    mkdir -p "$DATA_DIR"/{logs,images,pdfs,temp}
    print_success "Data directories created"
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t "$IMAGE_NAME" .
    print_success "Docker image built successfully"
}

# Stop and remove existing container
cleanup_container() {
    print_status "Cleaning up existing container..."
    if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
        docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
        print_success "Existing container cleaned up"
    fi
}

# Start the container
start_container() {
    print_status "Starting application..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$PORT:$PORT" \
        -v "$DATA_DIR:/app/data" \
        "$IMAGE_NAME" \
        streamlit run app.py --server.headless true --server.port $PORT
    print_success "Application started successfully"
}

# Show container status
show_status() {
    print_status "Container status:"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    print_success "Application is running at: http://localhost:$PORT"
    print_status "To view logs: docker logs -f $CONTAINER_NAME"
    print_status "To stop: docker stop $CONTAINER_NAME"
}

# Stop the container
stop_container() {
    print_status "Stopping application..."
    if docker ps --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
        print_success "Application stopped"
    else
        print_status "Application is not running"
    fi
}

# Show logs
show_logs() {
    print_status "Showing application logs..."
    docker logs -f "$CONTAINER_NAME"
}

# Main function
main() {
    case "${1:-start}" in
        "start")
            print_header
            check_docker
            create_directories
            build_image
            cleanup_container
            start_container
            show_status
            ;;
        "stop")
            print_header
            stop_container
            ;;
        "restart")
            print_header
            stop_container
            check_docker
            create_directories
            build_image
            start_container
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "build")
            print_header
            check_docker
            build_image
            print_success "Build completed"
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|logs|status|build}"
            echo ""
            echo "Commands:"
            echo "  start   - Build and start the application (default)"
            echo "  stop    - Stop the application"
            echo "  restart - Stop, rebuild, and start the application"
            echo "  logs    - Show application logs"
            echo "  status  - Show container status"
            echo "  build   - Build the Docker image only"
            exit 1
            ;;
    esac
}

main "$@"
