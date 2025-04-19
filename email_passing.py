import openai
import requests
import json

# Define the API key and the URL endpoint for chat/completions using AI Proxy
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDE1MTJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.eQHDm_FyNRaRsq-zl6_lkjCbeps3wPp9xPgny-lNBTo"  # Replace with your actual API key
url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # Custom proxy URL

# Path to the email file and output file
email_file_path = r"data/email.txt"
output_file_path = r"data/email-sender.txt"

# Read the email content from the file
with open(email_file_path, 'r') as email_file:
    email_content = email_file.read()

# Define the prompt for extracting the sender's email address
prompt = f"Extract the sender's email address from the following email message:\n\n{email_content}"

# Prepare the headers and payload for the request to the proxy
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",  # Specify the model
    "messages": [
        {"role": "system", "content": "You are an assistant that extracts email addresses from email content."},
        {"role": "user", "content": prompt}
    ]
}

# Make the API call to the custom AI Proxy
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the response was successful
if response.status_code == 200:
    # Parse the JSON response to extract the email
    response_data = response.json()
    extracted_email = response_data['choices'][0]['message']['content'].strip()

    # Write the extracted email address to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(extracted_email)

    print(f"Sender's email address extracted and saved to {output_file_path}")
else:
    # Handle errors if the request fails
    print(f"Error: Unable to extract email address. Status Code: {response.status_code}")
    print("Response:", response.text)
