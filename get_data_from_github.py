import requests

url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
response = requests.get(url)

with open("data_gen.py", "wb") as file:
    file.write(response.content)
