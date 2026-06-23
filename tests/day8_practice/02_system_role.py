import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "You are Spidey AI, a friendly and witty AI assistant. You speak like Spider-Man and use web/spider references. Keep answers short and fun."
        },
        {
            "role": "user",
            "content": "Who are you?"
        }
    ]
)

answer = response.choices[0].message.content
print(f"Spidey: {answer}")
