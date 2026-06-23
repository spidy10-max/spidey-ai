import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("=== WITHOUT History (AI bhool jata hai) ===")

response1 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "My name is Kasha"}
    ]
)
print(f"AI: {response1.choices[0].message.content}")

response2 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "What is my name?"}
    ]
)
print(f"AI: {response2.choices[0].message.content}")

print()
print("=== WITH History (AI yaad rakhta hai) ===")

messages = [
    {"role": "system", "content": "You are Spidey AI assistant."},
    {"role": "user", "content": "My name is Kasha"},
]

response3 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages
)
ai_reply = response3.choices[0].message.content
print(f"AI: {ai_reply}")

messages.append({"role": "assistant", "content": ai_reply})
messages.append({"role": "user", "content": "What is my name?"})

response4 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages
)
print(f"AI: {response4.choices[0].message.content}")
