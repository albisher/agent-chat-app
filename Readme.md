# Ollama Chat App

This is a simple chat application that allows you to chat with the Ollama language model (specifically Llama 3.1:1b) locally using a Streamlit UI.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd OLLAMA-CHAT-APP
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    Open your web browser and go to `http://localhost:8501`.

## Project Structure

-   `backend/`: Contains the backend API code (FastAPI).
-   `frontend/`: Contains the frontend UI code (Streamlit) and its own `requirements.txt` for specific dependencies.
-   `ollama/`: Contains the Dockerfile for building the Ollama image then downloading llama3.2:1b.
-   `docker-compose.yml`: Defines the services and their configurations.
-   `README.md`: This file.

## Notes

-   The initial startup might take some time as Docker builds the images and downloads the Ollama model.
-   You can customize the backend URL in `frontend/config.py` if needed.
-   You can add more features like user authentication, chat history persistence, etc.