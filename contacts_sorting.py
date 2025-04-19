import json

# Read the contacts data from the file
with open('data\contacts.json', 'r') as file:
    contacts = json.load(file)

# Sort the contacts by last_name and first_name
sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

# Write the sorted contacts back to a new JSON file
with open('data\contacts-sorted.json', 'w') as file:
    json.dump(sorted_contacts, file, indent=4)
