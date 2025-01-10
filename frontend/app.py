import streamlit as st
import requests
import json
from config import BACKEND_URL
from utils import process_response

# Set page title and favicon
st.set_page_config(page_title="Ollama Chat App", page_icon=":speech_balloon:")

# Sidebar for settings (optional)
with st.sidebar:
    st.header("Settings")
    # Add any settings you want here (e.g., API keys, model selection)

# Main chat interface
st.title("Ollama Chat App")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare data for backend request
    chat_history = [
        (msg["content"])
        for msg in st.session_state.messages
        if msg["role"] != "assistant"
    ]

    data = {
        "message": prompt,
        "history": chat_history,
    }

    # Send request to backend
    with st.spinner("Thinking..."):
        try:
            response = requests.post(BACKEND_URL, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for bad status codes
            response_json = response.json()
            response_content = process_response(response_json)
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with backend: {e}")
            response_content = None
        except json.JSONDecodeError as e:
            st.error(f"Error decoding backend response: {e}")
            response_content = None

    # Display assistant response
    if response_content:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response_content.split():
                full_response += chunk + " "
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )