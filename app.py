from flask import Flask, request, render_template, redirect, url_for, flash
import subprocess
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flash messages

# Set up logging
logging.basicConfig(filename='/var/log/honeypot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'admin'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return render_template('login.html'), 401  # Explicitly set status code for errors

    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

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
    
    return render_template('vulnerable.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
