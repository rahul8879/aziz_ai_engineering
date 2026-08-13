from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app import run_chat_turn
app = FastAPI(title="Fintech API", version="1.0.0")

# you need to handle cross origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    # you can return the html page
    return HTMLResponse(content=open("index.html").read())


@app.get("/chat")
def chat(user_message: str, session_id: str):
    response = run_chat_turn(user_message, session_id)
    return {"response": response}
