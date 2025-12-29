import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple test request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Say hello in one sentence"}
    ]
)

print("✅ OpenAI Response:")
print(response.choices[0].message.content)
