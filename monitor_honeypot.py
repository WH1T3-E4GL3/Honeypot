import time
import re

def tail_f(filename, interval=1.0):
    """Tails a file in real-time."""
    with open(filename, 'r') as f:
        # Go to the end of the file
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(interval)
                continue
            yield line

def parse_log_line(line):
    """Parses a log line and extracts relevant information."""
    log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\S+) - - \[(.*?)\] \"(\S+) (\S+) HTTP/(\S+)\" (\d+) (\S+)"
    command_pattern = r"Received command: (\S+)"
    command_output_pattern = r"Command output: (.*)"

    match = re.match(log_pattern, line)
    if match:
        timestamp, ip_address, request_time, method, path, http_version, status, reason = match.groups()
        command = None
        command_output = None
        return timestamp, ip_address, method, path, status, reason, command, command_output

    match = re.match(command_pattern, line)
    if match:
        command = match.group(1)
        return None, None, None, None, None, None, command, None

    match = re.match(command_output_pattern, line)
    if match:
        command_output = match.group(1)
        return None, None, None, None, None, None, None, command_output

    return None, None, None, None, None, None, None, None

def print_table_header(column_widths):
    """Prints the table header with dynamic column widths."""
    header_row = ""
    separator_row = ""
    for column, width in column_widths.items():
        header_row += f"{column:<{width}} | "
    print(header_row[:-3])  # Remove trailing ' | '
    print(separator_row[:-3])

def colorize_output(output_line, status):
    """Colorizes the output line based on status code."""
    if status == '404':
        return f"\033[93m{output_line}\033[0m"  # Yellow for 404
    return output_line

def monitor_log_file(logfile):
    """Monitors the log file and prints new entries in a table format."""
    print(f"Monitoring {logfile} for new entries...\n")

    column_names = ["Timestamp", "IP Address", "Method", "Path", "Status", "Reason", "Command", "Command Output"]
    column_widths = {column: len(column) for column in column_names}
    
    # Print header once
    print_table_header(column_widths)

    for line in tail_f(logfile):
        line = line.strip()
        timestamp, ip_address, method, path, status, reason, command, command_output = parse_log_line(line)
        
        if any((timestamp, ip_address, method, path, status, reason, command, command_output)):
            # Update column widths dynamically
            for column, value in zip(column_names, (timestamp, ip_address, method, path, status, reason, command, command_output)):
                if value:
                    column_widths[column] = max(column_widths[column], len(str(value)))
            
            # Build output line
            output_line = ""
            for column in column_names:
                value = locals().get(column.lower().replace(" ", "_"))
                output_line += f"{str(value) if value else '':<{column_widths[column]}} | "
            output_line = output_line[:-3]  # Remove trailing ' | '

            # Colorize based on status
            output_line = colorize_output(output_line, status)
            print(output_line)

if __name__ == "__main__":
    # Path to your honeypot log file
    log_file_path = '/var/log/honeypot.log'

    monitor_log_file(log_file_path)
