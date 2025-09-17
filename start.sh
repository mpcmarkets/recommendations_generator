#!/bin/bash

# Investment Recommendation Generator - Quick Start
# Simple entry point that delegates to the main deployment script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the main deployment script with all arguments
exec "$SCRIPT_DIR/scripts/deploy.sh" "$@"
