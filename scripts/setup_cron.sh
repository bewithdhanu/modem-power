#!/bin/bash

# Script to set up cron jobs for ModemPower
# Run this script to configure all cron jobs

PROJECT_DIR="/Volumes/T7/PycharmProjects/ModemPower"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

echo "Setting up cron jobs for ModemPower..."

# Create a temporary cron file
TEMP_CRON="/tmp/modem_power_cron"

# Get current crontab
crontab -l > "$TEMP_CRON" 2>/dev/null || touch "$TEMP_CRON"

# Remove any existing ModemPower cron jobs
grep -v "ModemPower" "$TEMP_CRON" > "$TEMP_CRON.new"
mv "$TEMP_CRON.new" "$TEMP_CRON"

# Add new cron jobs
cat >> "$TEMP_CRON" << EOF

# ModemPower Cron Jobs
# Start service on system startup (every reboot)
@reboot $SCRIPTS_DIR/start_service.sh

# Turn off device on system startup (every reboot)
@reboot sleep 30 && $SCRIPTS_DIR/turn_off_device.sh

# Turn off device on system shutdown (every day at 23:59)
59 23 * * * $SCRIPTS_DIR/turn_off_device.sh

# Run automate-modem every 5 minutes
*/5 * * * * $SCRIPTS_DIR/automate_modem.sh

# Restart service daily at 2 AM (to ensure it keeps running)
0 2 * * * $SCRIPTS_DIR/start_service.sh

EOF

# Install the new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "Cron jobs have been set up successfully!"
echo ""
echo "Installed cron jobs:"
echo "1. Start service on system startup"
echo "2. Turn off device on system startup (after 30 seconds)"
echo "3. Turn off device daily at 23:59"
echo "4. Run automate-modem every 5 minutes"
echo "5. Restart service daily at 2 AM"
echo ""
echo "To view your cron jobs, run: crontab -l"
echo "To remove all ModemPower cron jobs, run: crontab -e and remove lines containing 'ModemPower'"
