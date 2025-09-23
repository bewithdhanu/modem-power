#!/bin/bash

# Script to call automate-modem API every 5 minutes
# This script will be called by cron every 5 minutes

# Set the project directory
PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source venv/bin/activate

# Make API call to automate modem
curl -s "http://127.0.0.1:5000/automate-modem" > /dev/null 2>&1

# Log the action
echo "$(date): Automate modem script executed" >> "$PROJECT_DIR/logs/cron.log"
