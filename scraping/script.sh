#!/bin/bash

# Full path to your Python script
PYTHON_SCRIPT="/root/scraping/scraping.py"

# Change directory to the script's directory
cd "$(dirname "$PYTHON_SCRIPT")"
# Run file
python3 "$(basename "$PYTHON_SCRIPT")" > log.txt
