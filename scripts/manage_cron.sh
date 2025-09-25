#!/bin/bash

# Script to manage ModemPower cron jobs
# Usage: ./manage_cron.sh [setup|status|remove|start-service|stop-service]

PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

case "$1" in
    "setup")
        echo "Setting up ModemPower cron jobs..."
        $SCRIPTS_DIR/setup_cron.sh
        ;;
    "status")
        echo "Current ModemPower cron jobs:"
        echo "================================"
        crontab -l | grep -A 10 -B 2 "ModemPower" || echo "No ModemPower cron jobs found"
        echo ""
        echo "Service status:"
        if pgrep -f "python.*service.py" > /dev/null; then
            echo "✅ Flask service is running"
        else
            echo "❌ Flask service is not running"
        fi
        ;;
    "remove")
        echo "Removing ModemPower cron jobs..."
        crontab -l | grep -v "ModemPower" | crontab -
        echo "All ModemPower cron jobs removed"
        ;;
    "start-service")
        echo "Starting Flask service..."
        $SCRIPTS_DIR/start_service.sh
        ;;
    "stop-service")
        echo "Stopping Flask service..."
        pkill -f "python.*service.py"
        echo "Flask service stopped"
        ;;
    "restart-service")
        echo "Restarting Flask service..."
        pkill -f "python.*service.py" 2>/dev/null || true
        sleep 2
        $SCRIPTS_DIR/start_service.sh
        ;;
    *)
        echo "Usage: $0 [setup|status|remove|start-service|stop-service|restart-service]"
        echo ""
        echo "Commands:"
        echo "  setup         - Set up all ModemPower cron jobs"
        echo "  status        - Show current cron jobs and service status"
        echo "  remove        - Remove all ModemPower cron jobs"
        echo "  start-service - Start the Flask service manually"
        echo "  stop-service  - Stop the Flask service"
        echo "  restart-service - Restart the Flask service"
        ;;
esac
