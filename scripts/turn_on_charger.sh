#!/bin/bash

# Script to turn on charger via API
# This script will be called on computer startup/shutdown

# Set the project directory
PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source venv/bin/activate

# Make API call to turn on charger
curl -s "http://127.0.0.1:8765/turn-on-charger" > /dev/null 2>&1

# Log the action
echo "$(date): Charger turn-on script executed" >> "$PROJECT_DIR/logs/cron.log"
