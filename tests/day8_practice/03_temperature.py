import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

question = "Give me a creative name for an AI assistant"

print("=== Temperature 0.0 (Focused) ===")
response1 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": question}],
    temperature=0.0
)
print(response1.choices[0].message.content)

print()

print("=== Temperature 1.5 (Creative) ===")
response2 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": question}],
    temperature=1.5
)
print(response2.choices[0].message.content)
