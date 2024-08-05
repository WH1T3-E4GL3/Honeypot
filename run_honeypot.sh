# HoneyPot Implementation
# Author: Sethu Satheesh
# Created: 5/08/2024
# Modified: 5/08/2024


#!/bin/bash

# Start Flask app and redirect output to a log file
echo "Starting Flask app..."
nohup python app.py > flask.log 2>&1 &

# Start SSH service
echo "Starting SSH service..."
sudo service ssh start

# Check if Flask is running
sleep 2  # Give some time for Flask to start
echo "Checking Flask status..."
curl -I http://localhost:80

echo "Honeypot is running with HTTP on port 80 and SSH on port 22"
