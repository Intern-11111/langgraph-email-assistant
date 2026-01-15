import json
from pathlib import Path

MEMORY_FILE = Path("data/agent_state.json")


def save_state(state: dict):
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_state():
    if not MEMORY_FILE.exists():
        return None

    # Handle empty or corrupted JSON safely
    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    except json.JSONDecodeError:
        return None
