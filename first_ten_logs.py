import os

# Get a list of all .log files in the /data/logs/ directory
log_directory = "data\logs"
log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]

# Sort the log files by modification time (most recent first)
log_files.sort(key=lambda f: os.path.getmtime(os.path.join(log_directory, f)), reverse=True)

# Open the output file to write the first lines
with open('data\logs-recent.txt', 'w') as output_file:
    # Get the first line of the 10 most recent log files
    for log_file in log_files[:10]:
        log_file_path = os.path.join(log_directory, log_file)
        with open(log_file_path, 'r') as file:
            first_line = file.readline().strip()  # Read the first line
            output_file.write(first_line + '\n')  # Write it to the output file
