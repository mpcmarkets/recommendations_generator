#!/bin/bash

# Investment Recommendation Generator - Deployment Script
# This script handles deployment with ai_tools wheel file

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AI_TOOLS_WHEEL="ai_tools-1.0.0-py3-none-any.whl"
AI_TOOLS_SOURCE="../ai_tools/dist/${AI_TOOLS_WHEEL}"

print_header() {
    echo -e "\n${BLUE}🚀 Investment Recommendation Generator - Deployment${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_status() {
    echo -e "${YELLOW}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}📋 $1${NC}"
}

check_requirements() {
    print_status "Checking requirements..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check if pip is available
    if ! command -v pip &> /dev/null; then
        print_error "pip is not installed"
        exit 1
    fi
    
    print_success "Requirements check passed"
}

copy_ai_tools_wheel() {
    print_status "Setting up ai_tools wheel file..."
    
    if [ -f "$AI_TOOLS_SOURCE" ]; then
        cp "$AI_TOOLS_SOURCE" .
        print_success "ai_tools wheel file copied"
    else
        print_error "ai_tools wheel file not found at $AI_TOOLS_SOURCE"
        print_info "Building ai_tools wheel file..."
        cd ../ai_tools
        python -m build
        cd ../recommendation_generator
        if [ -f "$AI_TOOLS_SOURCE" ]; then
            cp "$AI_TOOLS_SOURCE" .
            print_success "ai_tools wheel file built and copied"
        else
            print_error "Failed to build ai_tools wheel file"
            exit 1
        fi
    fi
}

install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install ai_tools wheel first
    pip install --no-cache-dir "$AI_TOOLS_WHEEL"
    print_success "ai_tools installed"
    
    # Install other requirements
    pip install --no-cache-dir -r requirements.txt
    print_success "All dependencies installed"
}

setup_environment() {
    print_status "Setting up environment..."
    
    # Create data directories
    mkdir -p data/{logs,images,pdfs,temp}
    print_success "Data directories created"
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        print_info "No .env file found. Creating template..."
        cat > .env << EOF
# AI Tools Configuration
# Add your API keys here

OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
TAVILY_API_KEY=your_tavily_key_here
EOF
        print_info "Template .env file created. Please add your API keys."
    else
        print_success ".env file found"
    fi
}

test_installation() {
    print_status "Testing installation..."
    
    # Test ai_tools import
    if python3 -c "from ai_tools import LLMFactory; print('ai_tools import successful')" 2>/dev/null; then
        print_success "ai_tools import test passed"
    else
        print_error "ai_tools import test failed"
        exit 1
    fi
    
    # Test AI service
    if python3 -c "from services.ai_service import AIService; print('AI service import successful')" 2>/dev/null; then
        print_success "AI service import test passed"
    else
        print_error "AI service import test failed"
        exit 1
    fi
    
    # Test app import
    if python3 -c "import app; print('App import successful')" 2>/dev/null; then
        print_success "App import test passed"
    else
        print_error "App import test failed"
        exit 1
    fi
}

show_usage() {
    print_info "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h          Show this help message"
    echo "  --test-only         Only run tests, don't install"
    echo "  --no-test           Skip tests after installation"
    echo "  --clean             Clean previous installation first"
    echo ""
    echo "Examples:"
    echo "  $0                  # Full deployment"
    echo "  $0 --test-only      # Test existing installation"
    echo "  $0 --clean          # Clean install"
}

clean_installation() {
    print_status "Cleaning previous installation..."
    
    # Remove ai_tools if installed
    pip uninstall -y ai_tools 2>/dev/null || true
    
    # Remove wheel file
    rm -f "$AI_TOOLS_WHEEL"
    
    print_success "Cleanup completed"
}

run_tests() {
    print_status "Running comprehensive tests..."
    
    # Test AI service initialization
    if python3 -c "
from services.ai_service import AIService
ai = AIService()
print(f'AI Service available: {ai.is_available}')
" 2>/dev/null; then
        print_success "AI service initialization test passed"
    else
        print_error "AI service initialization test failed"
        return 1
    fi
    
    print_success "All tests passed"
}

main() {
    local test_only=false
    local no_test=false
    local clean=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_usage
                exit 0
                ;;
            --test-only)
                test_only=true
                shift
                ;;
            --no-test)
                no_test=true
                shift
                ;;
            --clean)
                clean=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    print_header
    
    if [ "$test_only" = true ]; then
        run_tests
        exit 0
    fi
    
    if [ "$clean" = true ]; then
        clean_installation
    fi
    
    check_requirements
    copy_ai_tools_wheel
    install_dependencies
    setup_environment
    
    if [ "$no_test" = false ]; then
        test_installation
        run_tests
    fi
    
    print_success "Deployment completed successfully!"
    print_info "To start the application: streamlit run app.py"
    print_info "To run with Docker: docker-compose up"
}

# Run main function with all arguments
main "$@"
