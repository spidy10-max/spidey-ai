from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Key found: {api_key[:10]}...")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello, I am Spidey AI!"
)

print("✅ Gemini is working!")
print(f"Response: {response.text}")
