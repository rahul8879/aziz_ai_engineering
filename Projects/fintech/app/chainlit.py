# lets use the chainlit to make UI
import chainlit as cl
import requests

BASE_URL = "http://127.0.0.1:8000"

def chat_with_api(user_message):
    response = requests.get(f"{BASE_URL}/chat", params={"user_message": user_message, "session_id": "default"})
    return response.json()

