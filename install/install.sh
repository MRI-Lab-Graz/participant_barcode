#!/bin/bash

# Exit on error
set -e

echo "Setting up Participant Barcode Tool..."

# Check for UV
if ! command -v uv &> /dev/null; then
    echo "UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create virtual environment in root using UV
if [ ! -d "../venv" ]; then
    echo "Creating virtual environment..."
    uv venv ../venv
fi

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r "$(dirname "$0")/requirements.txt"

echo "Setup complete!"
echo "To start the application, run: source venv/bin/activate && python app.py"
