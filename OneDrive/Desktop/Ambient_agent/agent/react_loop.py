# agent/react_loop.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from tools.calendar import read_calendar
from tools.contacts import lookup_contact
import uuid
import json

# ---------------- STATE ---------------- #
class AgentState(TypedDict):
    query: str
    thoughts: List[str]
    action: str
    observation: str
    trace_id: str
    result: str


# ---------------- REASON NODE ---------------- #
def reason_node(state: AgentState):

    query = state["query"].lower()
    thoughts = state.get("thoughts", [])

    if "calendar" in query:
        action = "read_calendar"

    elif "email" in query or "contact" in query:
        action = "lookup_contact"

    else:
        action = "none"

    thoughts.append(f"Reasoning: Based on query → I should use {action}")

    state["action"] = action
    state["thoughts"] = thoughts

    return state


# ---------------- TOOL EXECUTOR NODE ---------------- #
def tool_node(state: AgentState):

    action = state["action"]
    observation = ""

    if action == "read_calendar":
        observation = read_calendar()

    elif action == "lookup_contact":
        name = state["query"].split()[-1]  # last word as name
        observation = lookup_contact(name)

    else:
        observation = {"message": "No valid action required."}

    state["observation"] = str(observation)
    state["thoughts"].append(f"Tool Output: {observation}")

    return state


# ---------------- FINAL NODE ---------------- #
def final_node(state: AgentState):

    response = {
        "trace_id": state["trace_id"],
        "query": state["query"],
        "reasoning": state["thoughts"],
        "observation": state["observation"]
    }

    state["result"] = json.dumps(response, indent=2)

    return state


# ---------------- GRAPH BUILDER ---------------- #
def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("reason", reason_node)
    graph.add_node("act", tool_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("reason")

    graph.add_edge("reason", "act")
    graph.add_edge("act", "final")
    graph.add_edge("final", END)

    return graph.compile()


# ---------------- CLI RUNNER ---------------- #
if __name__ == "__main__":

    app = build_graph()

    user_input = input("\nEnter your query: ")

    input_state = {
        "query": user_input,
        "thoughts": [],
        "action": "",
        "observation": "",
        "trace_id": str(uuid.uuid4()),
        "result": ""
    }

    result = app.invoke(input_state)

    print("\n--- Agent Output (JSON) ---")
    print(result["result"])
