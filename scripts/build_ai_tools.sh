#!/bin/bash

# Build ai_tools wheel from source
# This script builds the ai_tools package from the included source code

set -euo pipefail

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

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

log_info "Building ai_tools wheel from source..."

# Create temporary directory for building
TEMP_DIR=$(mktemp -d)
log_info "Using temporary directory: $TEMP_DIR"

# Copy ai_tools source to temp directory
cp -r "$PROJECT_DIR/ai_tools_source" "$TEMP_DIR/ai_tools"
cp "$PROJECT_DIR/ai_tools_setup.py" "$TEMP_DIR/setup.py"
cp "$PROJECT_DIR/ai_tools_pyproject.toml" "$TEMP_DIR/pyproject.toml"
cp "$PROJECT_DIR/ai_tools_requirements.txt" "$TEMP_DIR/requirements.txt"

# Build the wheel
cd "$TEMP_DIR"
log_info "Installing build dependencies..."
pip install build

log_info "Building wheel..."
python -m build

# Copy the built wheel back to project directory
WHEEL_FILE=$(find dist -name "*.whl" | head -1)
if [ -n "$WHEEL_FILE" ]; then
    cp "$WHEEL_FILE" "$PROJECT_DIR/"
    log_success "Built wheel: $(basename "$WHEEL_FILE")"
else
    log_error "No wheel file found in dist/"
    exit 1
fi

# Clean up
cd "$PROJECT_DIR"
rm -rf "$TEMP_DIR"

log_success "ai_tools wheel built successfully!"
log_info "Wheel file: $(basename "$WHEEL_FILE")"
