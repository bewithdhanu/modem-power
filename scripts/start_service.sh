#!/bin/bash

# Script to start the Flask service in background
# This script will be called on computer startup

# Set the project directory
PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source venv/bin/activate

# Check if service is already running
if pgrep -f "python.*service.py" > /dev/null; then
    echo "$(date): Service already running" >> "$PROJECT_DIR/logs/cron.log"
    exit 0
fi

# Start the service in background
nohup python service.py > "$PROJECT_DIR/logs/service.log" 2>&1 &

# Log the action
echo "$(date): Service started in background" >> "$PROJECT_DIR/logs/cron.log"
