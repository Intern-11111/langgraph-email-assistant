from langchain_core.messages import AIMessage

def triage_node(state):
    print("--- TRIAGING EMAIL ---")
    return {"triage_category": "respond-act"}

def check_route(state):
    return state.get("triage_category", "ignore")

def react_model_node(state):
    print("--- AGENT IS THINKING ---")
    # Simulating a tool call
    return {"messages": [AIMessage(content="I should use a tool to send this.")]}

def react_route(state):
    # Logic to decide if we go to tools or end
    return "react_tools"

def react_tools_node(state):
    print("--- EXECUTING TOOLS (ACTION) ---")
    return {"final_reply": "Email sent successfully!"}

def ignore(state):
    print("--- IGNORING EMAIL ---")
    return state

def notify_human(state):
    print("--- NOTIFYING HUMAN ---")
    return state
