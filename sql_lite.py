import sqlite3

# Define the database path
db_path = r"data\ticket-sales.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to calculate total sales for "Gold" ticket type
query = """
    SELECT SUM(units * price) 
    FROM tickets 
    WHERE type = 'Gold'
"""
cursor.execute(query)
total_sales = cursor.fetchone()[0]

# Close the database connection
conn.close()

# Define the output file path
output_path = r"data\ticket-sales-gold.txt"

# Write the total sales to the file
with open(output_path, "w") as file:
    file.write(str(total_sales))

# Return the total sales value
total_sales
