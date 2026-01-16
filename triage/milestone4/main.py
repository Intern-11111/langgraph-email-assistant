from graph import graph
from memory import memory

# Compile with memory + interrupt
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["tools"]
)

config = {
    "configurable": {
        "thread_id": "email_session_1"
    }
}

print("\n--- RUNNING EMAIL AGENT ---\n")

result = app.invoke(
    {"input": "Please approve my internship application."},
    config=config
)

print("\n--- EXECUTION PAUSED BEFORE TOOL ---") 