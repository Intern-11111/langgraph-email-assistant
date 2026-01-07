import json
from pathlib import Path

MEMORY_FILE = Path("data/agent_state.json")

def save_state(state: dict):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return None
