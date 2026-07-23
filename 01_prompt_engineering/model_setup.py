# to connect with open ai models
# 1. via api 2. via sdk (openai)
from dotenv import load_dotenv
from openai import OpenAI
print(load_dotenv())

client = OpenAI()
# documntations

def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # last training was around 2021
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


