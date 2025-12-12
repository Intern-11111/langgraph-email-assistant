from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("Using API KEY:", api_key)

if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment!")
    exit()

# Configure Google client manually
genai.configure(api_key=api_key)

print("\n--- Available Models For This API Key ---\n")

models = genai.list_models()
for m in models:
    print(m.name)
