from src.hitl.graph import build_hitl_graph
from src.hitl.memory import load_state

# Try to resume from saved state
saved_state = load_state()

if saved_state:
    print("Resuming agent from saved state:")
    print(saved_state)
else:
    print("Starting new agent run")
    saved_state = {
        "email": {
            "subject": "Urgent approval needed",
            "body": "Please approve the budget by EOD"
        }
    }

graph = build_hitl_graph()

result = graph.invoke(saved_state)

print("\nAgent execution paused.")
print("Current state:", result)
