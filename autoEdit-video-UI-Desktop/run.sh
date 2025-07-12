#!/bin/bash

echo "========================================"
echo "AutoEdit Video UI Desktop - Starting..."
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found!"
    exit 1
fi

# Run the application
echo "Starting AutoEdit Video UI Desktop..."
echo
python main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo
    echo "Application exited with error"
fi
