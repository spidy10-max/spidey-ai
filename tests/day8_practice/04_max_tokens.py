import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

question = "Explain what artificial intelligence is"

print("=== Max 50 Tokens (Short) ===")
response1 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": question}],
    max_tokens=50
)
print(response1.choices[0].message.content)

print()

print("=== Max 300 Tokens (Long) ===")
response2 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": question}],
    max_tokens=300
)
print(response2.choices[0].message.content)
