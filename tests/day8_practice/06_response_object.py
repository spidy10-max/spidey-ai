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
        {"role": "system", "content": "You are Spidey AI."},
        {"role": "user", "content": "Hello Spidey!"}
    ],
    temperature=0.7,
    max_tokens=100
)

print("=== Full Response Details ===")
print(f"Model used: {response.model}")
print(f"AI Reply: {response.choices[0].message.content}")
print(f"Role: {response.choices[0].message.role}")
print(f"Finish Reason: {response.choices[0].finish_reason}")
print(f"Input Tokens: {response.usage.prompt_tokens}")
print(f"Output Tokens: {response.usage.completion_tokens}")
print(f"Total Tokens: {response.usage.total_tokens}")
