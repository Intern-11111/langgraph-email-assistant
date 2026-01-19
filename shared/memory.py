import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(email, edited_response):
    memory = load_memory()
    memory[email] = edited_response
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
