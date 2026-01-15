from src.hitl.graph import build_hitl_graph
from src.hitl.memory import load_state

saved_state = load_state()

if saved_state:
    print("Resuming agent from saved state:")
    print(saved_state)
else:
    print("Starting new agent run")
    saved_state = {
        "email": {
            "subject": "Send project update",
            "body": "Please send the latest update to the client"
        }
    }

graph = build_hitl_graph()
result = graph.invoke(saved_state)

# 🔴 MILESTONE-4 USER NOTIFICATION
if result.get("triage_decision") == "respond":
    print("\n⚠️ HUMAN APPROVAL REQUIRED ⚠️")
    print("Sensitive tool detected: send_email")
    print("Agent execution paused before tool execution.")

print("\nAgent paused.")
print("Current state:", result)
