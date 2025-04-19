import requests
import json
import pytesseract
from PIL import Image

# Define the API key and the URL endpoint for chat/completions using AI Proxy
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDE1MTJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.eQHDm_FyNRaRsq-zl6_lkjCbeps3wPp9xPgny-lNBTo"  # Replace with your actual API key
url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # Custom proxy URL

# Path to the credit card image and output file
image_file_path = "data\credit_card.png"
output_file_path = "data\credit-card.txt"

# Function to extract text from the image using Tesseract OCR
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

# Extract text (credit card number) from the image
card_number_text = extract_text_from_image(image_file_path)

# If the extracted text has spaces, remove them
card_number = ''.join(card_number_text.split())

# Define the prompt to clean up the extracted card number if needed
prompt = f"Clean the following credit card number (remove spaces and format it correctly): {card_number}"

# Prepare the headers and payload for the request to the AI Proxy
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",  # Specify the model
    "messages": [
        {"role": "system", "content": "You are an assistant that formats credit card numbers correctly."},
        {"role": "user", "content": prompt}
    ]
}

# Make the API call to the custom AI Proxy
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the response was successful
if response.status_code == 200:
    # Parse the JSON response to extract the formatted card number
    response_data = response.json()
    cleaned_card_number = response_data['choices'][0]['message']['content'].strip()

    # Write the cleaned credit card number to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(cleaned_card_number)

    print(f"Credit card number extracted and saved to {output_file_path}")
else:
    # Handle errors if the request fails
    print(f"Error: Unable to extract and clean card number. Status Code: {response.status_code}")
    print("Response:", response.text)
