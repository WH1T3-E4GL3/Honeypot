# Honeypot Project

A simple honeypot implementation to capture and monitor malicious activity. This project uses Flask to create a vulnerable web application and sets up an SSH service for attackers to interact with. It includes logging and monitoring scripts to track and analyze the activity.

**_Project Ongoing...⌛_**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Monitoring](#monitoring)
- [Notes](#notes)
- [License](#license)

## Features

- Flask-based vulnerable web application
- SSH service configured with weak credentials
- Logging of commands executed via the web application
- Real-time monitoring of honeypot logs
- More features coming soon...⌛

0. **Pre Setup**
   
   Create a new user on your system for making that account as the Honeypot.
   
      sudo useradd -m -s /bin/bash vulnerableuser # change vulnerable user to your desired username
      sudo passwd vulnerableuser  # Set a weak password like 'password123 or admin or root'
   


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/WH1T3-E4GL3/Honeypot.git
    cd Honeypot
    ```

2. **Create and activate a Python virtual environment:**

    ```bash
    python -m venv honeypot-env
    source honeypot-env/bin/activate  # For Windows use `honeypot-env\Scripts\activate`
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install and configure SSH:**

    ```bash
    sudo apt-get install openssh-server
    sudo nano /etc/ssh/sshd_config
    ```

    Edit the SSH configuration file (`/etc/ssh/sshd_config`) to allow password authentication. Add or modify the following lines:

    ```
    PermitRootLogin yes
    PasswordAuthentication yes
    PermitEmptyPasswords yes  # Optional, but increases vulnerability
    ```

    Restart the SSH service:

    ```bash
    sudo systemctl restart ssh
    ```

## Setup

1. **Run the Flask application and SSH service:**

    ```bash
    sudo su
    ./run_honeypot.sh
    ```

2. **Monitor logs in real-time:**

    ```bash
    >> tail -f /var/log/auth.log  # For SSH logs
    or
    >> sudo journalctl -u ssh -f (if above command for ssh not works)
    or check ssh log in your system / monitor it live 
    
    >> tail -f /var/log/honeypot.log  # For Flask app logs
    ```

## Usage

- Access the vulnerable web application at [http://localhost](http://localhost)
- Use the `/vulnerable` endpoint to execute commands. For example:

    ```bash
    http://localhost/vulnerable?cmd=ls
    ```

- The output of commands and any errors will be logged in `/var/log/honeypot.log`.

## Monitoring

To monitor the honeypot activity, you can use the `monitor_honeypot.py` script:

    ```bash
    python monitor_honeypot.py
    ```

This script will print new log entries in a formatted table in real-time.

## Notes

- Make sure to adjust permissions and configurations based on your security needs.
- This setup is intentionally vulnerable for educational purposes and should not be used in a production environment.


