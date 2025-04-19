from fastapi import FastAPI, Query
import json
import datetime
import subprocess
import os
from openai import OpenAI
import requests
import sqlite3
import duckdb
from bs4 import BeautifulSoup
from PIL import Image
import markdown
# from faster_whisper import Whisper



app = FastAPI()


AIRPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # Replace with your actual AirProxy URL
API_KEY = os.getenv('AIPROXY_API')  # Replace with your API key if required

print(API_KEY)

def parse_task(task_description):
    """
    Uses an LLM (GPT-4 via AirProxy) to parse a natural language task into a structured JSON format.
    """
    prompt = f"""
    You are an AI agent that extracts structured instructions from natural language tasks.

    Task: {task_description}

    Extract the following:
    - Action (e.g., count, extract, sort, format, run script)
    - Input file(s)
    - Output file (if applicable)
    - Additional parameters

    Return as a JSON object.
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    
    response = requests.post(AIRPROXY_URL, json=payload, headers=headers)
    response_data = response.json()
    
    return json.loads(response_data["choices"][0]["message"]["content"])



def validate_file_path(filepath):
    """Ensure the file path is inside /data/."""
    abs_path = os.path.abspath(filepath)
    if not abs_path.startswith("/data/"):
        raise ValueError(f"Access to {filepath} is not allowed. Only /data/ directory is permitted.")

def execute_task(parsed_task):
    """Executes a task but prevents deletion or access outside /data/."""
    action = parsed_task["action"]
    input_file = parsed_task.get("input_file")
    output_file = parsed_task.get("output_file")

    # Validate file paths
    if input_file:
        validate_file_path(input_file)
    if output_file:
        validate_file_path(output_file)

    # Prevent deletion requests
    if action in ["delete_file", "remove_data"]:
        return "Operation not allowed: File deletion is restricted."

    # Route tasks to specific functions
    task_map = {
        "fetch_api": fetch_api_data,
        "clone_git": clone_git_repo,
        "run_sql": run_sql_query,
        "scrape_website": scrape_website,
        "resize_image": resize_image,
        "transcribe_audio": transcribe_audio,
        "convert_md_html": convert_markdown_to_html,
        "filter_csv": filter_csv_data
    }

    if action in task_map:
        return task_map[action](**parsed_task)
    else:
        return f"Action '{action}' not supported."


def count_wednesdays(input_file, output_file):
    """
    Counts the number of Wednesdays in a file containing dates.
    """
    with open(input_file, "r") as f:
        dates = f.readlines()

    count = sum(1 for date in dates if datetime.datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

    with open(output_file, "w") as f:
        f.write(str(count))
    return f"Counted {count} Wednesdays."

def sort_contacts(input_file, output_file):
    """
    Sorts contacts by last_name, then first_name.
    """
    with open(input_file, "r") as f:
        contacts = json.load(f)

    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Contacts sorted successfully."

def run_script(script_url, args):
    """
    Runs a Python script with optional arguments.
    """
    command = ["uv", "run", "python", script_url] + args
    subprocess.run(command, check=True)
    return "Script executed successfully."

@app.get("/run")
async def run_task(task: str = Query(..., description="Task description")):
    """
    API endpoint that takes a task description, parses it, and executes it.
    """
    parsed_task = parse_task(task)  # Parse task using LLM
    result = execute_task(parsed_task)  # Execute parsed task
    return {"task": task, "status": "completed", "result": result}


# B3
def fetch_api_data(api_url, output_file):
    """Fetch JSON data from an API and save it."""
    response = requests.get(api_url)
    if response.status_code == 200:
        with open(output_file, "w") as f:
            f.write(response.text)
        return f"API data saved to {output_file}"
    else:
        return f"API request failed with status code {response.status_code}"

# B4
import subprocess

def clone_git_repo(repo_url, commit_message, file_to_edit=None, new_content=None):
    """Clones a git repo, optionally modifies a file, and commits the change."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url, f"/data/{repo_name}"])
    
    if file_to_edit and new_content:
        validate_file_path(f"/data/{repo_name}/{file_to_edit}")  # Security check
        with open(f"/data/{repo_name}/{file_to_edit}", "w") as f:
            f.write(new_content)
        subprocess.run(["git", "add", file_to_edit], cwd=f"/data/{repo_name}")
        subprocess.run(["git", "commit", "-m", commit_message], cwd=f"/data/{repo_name}")
    
    return f"Repo {repo_name} cloned and modified."

# B5

def run_sql_query(db_type, db_file, query, output_file):
    """Executes a SQL query on SQLite or DuckDB and saves the results."""
    validate_file_path(db_file)
    
    if db_type == "sqlite":
        conn = sqlite3.connect(db_file)
    elif db_type == "duckdb":
        conn = duckdb.connect(db_file)
    else:
        return "Unsupported database type."

    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    with open(output_file, "w") as f:
        json.dump(results, f)

    conn.close()
    return f"SQL query executed and saved to {output_file}"



# B6
def scrape_website(url, output_file):
    """Scrapes a website and extracts text content."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text_content = soup.get_text()

    with open(output_file, "w") as f:
        f.write(text_content)

    return f"Website data saved to {output_file}"

#B7


def resize_image(input_file, output_file, width, height):
    """Resizes an image to specified dimensions."""
    validate_file_path(input_file)
    img = Image.open(input_file)
    img_resized = img.resize((width, height))
    img_resized.save(output_file)
    return f"Image resized and saved to {output_file}"

# B8




# def transcribe_audio(input_file, output_file):
#     model = Whisper("small")  # Load model once
#     segments, _ = model.transcribe(input_file)

#     with open(output_file, "w") as f:
#         for segment in segments:
#             f.write(segment.text + "\n")

#     return f"Transcription saved to {output_file}"


# B9

def convert_markdown_to_html(input_file, output_file):
    """Converts a Markdown file to HTML."""
    validate_file_path(input_file)
    with open(input_file, "r") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)

    with open(output_file, "w") as f:
        f.write(html_content)

    return f"Markdown converted to HTML and saved to {output_file}"


# B10
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/filter_csv")
def filter_csv_data(column: str, value: str):
    """Filters a CSV file by column and value, then returns JSON."""
    csv_file = "/data/data.csv"  # Assume fixed CSV path for security
    validate_file_path(csv_file)
    
    df = pd.read_csv(csv_file)
    filtered_df = df[df[column] == value]

    return filtered_df.to_dict(orient="records")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
