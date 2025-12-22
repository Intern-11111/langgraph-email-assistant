# list_models.py
from google import genai

client = genai.Client(api_key="YOUR_GOOGLE_API_KEY")  # put your key here
models = client.list_models()

for m in models:
    print(m.name, "-", m.supported_generation_methods)
