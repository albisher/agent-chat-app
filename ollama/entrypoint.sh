#!/bin/bash
ollama serve &  # Start Ollama in the background
sleep 5         # Give Ollama time to start
ollama pull llama3.2:1b   # Pull the model
wait $!        # Keep the container running