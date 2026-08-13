import streamlit as st
import requests
BASE_URL = "http://127.0.0.1:8000"
def chat_with_api(user_message):
    response = requests.get(f"{BASE_URL}/chat", params={"user_message": user_message, "session_id": "default"})
    return response.json()

st.title("Fintech Chatbot")
user_input = st.text_input("You: ", "")
if st.button("Send"):
    response = chat_with_api(user_input)
    st.text_area("AI: ", value=response.get("response", ""), height=300)
