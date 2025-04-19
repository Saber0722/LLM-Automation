import os
import json

# Path to the directory containing Markdown files
docs_directory = r"C:\Users\caaka\iCloudDrive\IITM\Assignments\TDS\Projects\Project_1\data\docs"

# List all .md files in the directory and its subdirectories
md_files = []
for root, _, files in os.walk(docs_directory):
    for file in files:
        if file.endswith('.md'):
            # Add the file's relative path (without the /data/docs/ prefix)
            relative_path = os.path.relpath(os.path.join(root, file), docs_directory)
            md_files.append(relative_path)

# Print the list of .md files found
print("Markdown files found:", md_files)

# Initialize a dictionary to store the index
index = {}

# Process each Markdown file
for md_file in md_files:
    file_path = os.path.join(docs_directory, md_file)
    with open(file_path, 'r') as file:
        # Read the lines of the file
        lines = file.readlines()
        # Find the first occurrence of an H1 (#)
        for line in lines:
            if line.startswith('# '):  # H1 starts with a single #
                # Extract the title (remove the # and any surrounding whitespace)
                title = line[2:].strip()
                print(f"Found title '{title}' in {md_file}")  # Debug print
                index[md_file] = title
                break  # Only take the first H1

# Check if the index is being populated
print("Index generated:", index)

# Write the index to a JSON file
with open(r'c:\Users\caaka\IcloudDrive\IITM\Assignments\TDS\Projects\Project_1\data\docs\index.json', 'w') as output_file:
    json.dump(index, output_file, indent=4)

print("Index saved to index.json")
