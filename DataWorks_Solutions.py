from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

# OpenAI API key
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDE1MTJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.eQHDm_FyNRaRsq-zl6_lkjCbeps3wPp9xPgny-lNBTo'

# URL for OpenAI's Chat Completion endpoint
openai_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# Define headers for the request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Define a Pydantic model to parse the request body
class TaskRequest(BaseModel):
    task_description: str

# Task 1: Executes a plain‑English task.
@app.post("/run")
async def run(request: TaskRequest):
    task_description = request.task_description

    # Prepare the message in the chat format (list of messages)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task_description}
    ]

    # Create the request payload for the OpenAI API
    data = {
        "model": "gpt-4o-mini",  # You can use other models like gpt-4
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.7
    }

    async with httpx.AsyncClient() as client:
        try:
            # Send the POST request to OpenAI's /v1/chat/completions endpoint
            response = await client.post(openai_url, json=data, headers=headers)
            
            # Check for a successful response
            if response.status_code == 200:
                result = response.json()
                # Extract the response text from OpenAI's response
                chat_response = result["choices"][0]["message"]["content"]
                return {"task_result": chat_response}
            else:
                raise HTTPException(status_code=response.status_code, detail="Error from OpenAI API")

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        

  # Task 2: Return the content of the specified file.      
@app.get("/read")
async def read_file(path: str):
    if os.path.exists(path):
        try:
            with open(path, "r") as file:
                content = file.read()
            return PlainTextResponse(content=content)  # Return the file content as plain text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
