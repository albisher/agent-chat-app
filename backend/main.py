from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

# Model for incoming chat messages
class ChatMessage(BaseModel):
    message: str
    history: list  # List of previous messages in the conversation

# Check if Ollama is available and pull the model if necessary
ollama_base_url = os.environ.get("OLLAMA_BASE_URL")
ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

def check_ollama_availability():
    try:
        response = requests.get(f"{ollama_base_url}/api/tags")
        response.raise_for_status()  # Raise an exception for bad status codes
        return True
    except requests.exceptions.ConnectionError:
        return False

def pull_ollama_model(model_name):
    try:
        # Note: POST request to /api/pull requires a model name in the body
        response = requests.post(f"{ollama_base_url}/api/pull", json={"name": model_name})
        response.raise_for_status()
        print(f"Model {model_name} pulled successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error pulling model {model_name}: {e}")

if check_ollama_availability():
    pull_ollama_model(ollama_model)
else:
    print("Ollama server is not available. Model pulling skipped.")

# Initialize Ollama model through LangChain
llm = Ollama(model=ollama_model, base_url=ollama_base_url)
output_parser = StrOutputParser()

# Create a simple prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful chatbot. Answer the user's question as best you can."),
    ("user", "{question}"),
])

# Create the LangChain chain
chain = prompt | llm | output_parser

@app.post("/chat")
async def chat_with_ollama(chat_message: ChatMessage):
    try:
        # Invoke the LangChain chain
        response = chain.invoke({"question": chat_message.message})

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))