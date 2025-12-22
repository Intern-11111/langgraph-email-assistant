from google import genai
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# List all models
pager = client.models.list()
for model in pager:
    print("Name:", model.name)
    # show all metadata to see what methods are supported
    if hasattr(model, "metadata"):
        print("Metadata:", model.metadata)
    print("-" * 40)
