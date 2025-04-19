import datetime

# Initialize the counter
wednesday_count = 0

# Open and read the dates from the file
with open('data\dates.txt', 'r') as file:
    for line in file:
        try:
            # Parse the date
            date = datetime.datetime.strptime(line.strip(), "%Y-%m-%d")
            # Check if the day is Wednesday (weekday() returns 2 for Wednesday)
            if date.weekday() == 2:
                wednesday_count += 1
        except ValueError:
            # Skip any lines that don't match the expected date format
            continue

# Write the count to the output file
with open('data\dates-wednesdays.txt', 'w') as output_file:
    output_file.write(str(wednesday_count))
