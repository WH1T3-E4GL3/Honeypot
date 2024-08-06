#!/bin/bash

# HoneyPot Implementation
# Author: Sethu Satheesh
# Created: 5/08/2024
# Modified: 6/08/2024

echo """
  _    _                          _____      _   
 | |  | |                        |  __ \    | |  
 | |__| | ___  _ __   ___ _   _  | |__) |__ | |_ 
 |  __  |/ _ \| '_ \ / _ \ | | | |  ___/ _ \| __|
 | |  | | (_) | | | |  __/ |_| | | |  | (_) | |_ 
 |_|  |_|\___/|_| |_|\___|\__, | |_|   \___/ \__|
                           __/ |                 
                          |___/   Auth: @whxite                
"""

# Check if necessary commands are available
for cmd in python nohup service curl date; do
    if ! command -v $cmd &> /dev/null; then
        echo >&2 "[$(date +'%b %d %H:%M:%S')] $(hostname) [ERROR] Command '$cmd' is required but not installed. Aborting."
        exit 1
    fi
done

# Function to log with timestamp
log() {
    echo "[$(date +'%b %d %H:%M:%S')] $(hostname) $1"
}

# Start Flask app and redirect output to a log file
log "[INFO] Started deploying Honeypot..."
log "[INFO] Starting Flask app [HTTP Service]..."
nohup python app.py > flask.log 2>&1 &
FLASK_PID=$!
log "[INFO] Flask app started with process ID: $FLASK_PID"

# Start SSH service
log "[INFO] Starting SSH service..."
sudo service ssh start

# Check if Flask is running
sleep 2  # Give some time for Flask to start
log "[INFO] Checking Flask status..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)

if [ $HTTP_STATUS -eq 200 ]; then
    log "[SUCCESS] Flask app is running on port 80. HTTP status: $HTTP_STATUS"
else
    log "[ERROR] Flask app is not running. HTTP status: $HTTP_STATUS"
    exit 1
fi

# Check SSH service status
SSH_STATUS=$(sudo service ssh status | grep -c 'running')
if [ $SSH_STATUS -gt 0 ]; then
    log "[SUCCESS] SSH service is running on port 22."
else
    log "[ERROR] SSH service failed to start."
    exit 1
fi

log "[INFO] Honeypot is deployed on network with HTTP on port 80 and SSH on port 22"
