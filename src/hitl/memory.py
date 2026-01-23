import json
import os

STATE_FILE = "data/agent_state.json"


def save_state(state):
    """
    Save agent state to disk.
    """
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def load_state():
    """
    Load agent state if exists.
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return None
