# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.src.nodes.node import triage_node, react_model_node, react_tools_node, react_route
from backend.src.state import AgentState

print("----------------NODE TESTS----------------") 

# Test 1: Triage (works!)
email = {"subject": "Meeting Tuesday 10AM?", "body": "Are you free?"}
state = {"mail": email}
triage = triage_node(state)
print(f"Triage: {triage}")

# Test 2: ReAct - FULL STATE
react_state = {
    "mail": email,
    "messages": [],  
    "triage_category": "respond-act"
}
react_result = react_model_node(react_state)
print(f"Tool detected: {react_result.get('tool_name', 'None')}")
print(f"Tool args: {react_result.get('tool_args', 'None')}")

# Test 3: Tools execute
if react_result.get('tool_name'):
    tools_result = react_tools_node(react_result)
    print(f"Tool result: {tools_result['messages'][-1].content}")

# Test 4: HITL dangerous route
dangerous_state = {
    "tool_name": "send_gmail_reply",  
    "messages": []
}
route = react_route(dangerous_state)
print(f"Dangerous route: {route}")  

print("Nodes ready ✓")