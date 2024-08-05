# Vulnerable HoneyPot
# Author: Sethu Satheesh
# Created: 5/08/2024
# Modified: 5/08/2024

from flask import Flask, request
import subprocess
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='/var/log/honeypot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/vulnerable', methods=['GET'])
def vulnerable():
    cmd = request.args.get('cmd')
    if cmd:
        try:
            # Log the received command
            logging.info(f"Received command: {cmd}")
            
            # Execute the command with shell=True
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Capture the output
            output = result.stdout + result.stderr
            
            # Log the command output
            logging.info(f"Command output: {output}")
            
        except Exception as e:
            output = f"Error: {str(e)}"
            logging.error(f"Error executing command: {e}")
    else:
        output = 'No command provided'
    return '<pre>{}</pre>'.format(output)

@app.route('/')
def home():
    return 'Welcome to the vulnerable web application!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
