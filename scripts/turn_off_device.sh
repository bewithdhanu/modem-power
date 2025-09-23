#!/bin/bash

# Script to turn off device via API
# This script will be called on computer startup/shutdown

# Set the project directory
PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source venv/bin/activate

# Make API call to turn off device
curl -s "http://127.0.0.1:5000/turn-off-device" > /dev/null 2>&1

# Log the action
echo "$(date): Device turn-off script executed" >> "$PROJECT_DIR/logs/cron.log"
