import sqlite3
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.types import interrupt, Command

# --- 1. STATE DEFINITION ---
class AgentState(TypedDict):
    # add_messages logic (simulated by list addition)
    messages: Annotated[list[BaseMessage], lambda x, y: x + y]
    user_id: str

# --- 2. MEMORY HELPERS (Long-term Learning) ---
def get_user_prefs(store: BaseStore, user_id: str):
    namespace = (user_id, "preferences")
    item = store.get(namespace, "user_profile")
    return item.value if item else "No preferences yet."

def save_user_pref(store: BaseStore, user_id: str, feedback: str):
    namespace = (user_id, "preferences")
    current = get_user_prefs(store, user_id)
    # The 'Learning' part: appending new knowledge to the Store
    store.put(namespace, "user_profile", f"{current} | Correction: {feedback}")

# --- 3. NODES -----

def assistant(state: AgentState, store: BaseStore):
    """
    Load preferences from memory.
    Simulates an LLM drafting an email based on stored memory.
    """
    user_id = state["user_id"]
    prefs = get_user_prefs(store, user_id)
    
    # Logic: If 'Robert' is in memory, use it. Otherwise, use 'Bob'.
    name_to_use = "Robert" if "Robert" in prefs else "Bob"
    
    # LLM Response
    content = f"Subject: Sync Up. Hi {name_to_use}, let's meet tomorrow."
    return {"messages": [AIMessage(content=content)]}

def human_review_node(state: AgentState, store: BaseStore):
    """
    Flag unsafe tools, Configure Interrupts, and Notify User.
    """
    last_draft = state["messages"][-1].content
    
    print(f"\n--- [ALERT: HUMAN APPROVAL REQUIRED] ---")
    print(f"Draft to Review: {last_draft}")
    
    #Pause execution using interrupt()
    human_input = interrupt({
        "action": "Review Draft",
        "current_draft": last_draft
    })

    #Deliverable - Learning from "Edit"
    if human_input.get("type") == "edit":
        feedback = human_input.get("feedback")
        save_user_pref(store, state["user_id"], feedback)
        print(f"Memory Updated: Persistent Store now remembers: '{feedback}'")
        
        # Resume and go back to assistant to redraw with new memory
        return Command(
            goto="assistant",
            update={"messages": [HumanMessage(content=f"Updating based on: {feedback}")]}
        )
    
    print(">>> Final Action: Email sent")
    return Command(goto=END)

# --- 4. GRAPH CONSTRUCTION ---


builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("human_review", human_review_node)

builder.add_edge(START, "assistant")
builder.add_edge("assistant", "human_review") # Force review for all drafts

# Persistent Database
# This creates a local file 'm4.db' that saves progress
conn = sqlite3.connect("m4.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
persistent_store = InMemoryStore()

# Compile with checkpointer 
graph = builder.compile(checkpointer=checkpointer, store=persistent_store)

# ---EXECUTION STEP BY STEP ---
def run_milestone_demo():
    # Manage Thread IDs
    thread_config = {"configurable": {"thread_id": "milestone_4_thread"}}
    uid = "student_user_1"

    print("\n--- TEST 1: Initial Draft (Agent doesn't know Robert yet) ---")
    inputs = {"messages": [HumanMessage(content="Email Bob.")], "user_id": uid}
    
    # Run until the interrupt
    for event in graph.stream(inputs, thread_config):
        pass

    # Human Input: 'edit' to teach the agent
    print("\n[USER PROVIDES FEEDBACK]: 'Actually, his name is Robert, not Bob.'")
    # This resumes the graph
    feedback_cmd = Command(resume={"type": "edit", "feedback": "His name is Robert."})
    
    for event in graph.stream(feedback_cmd, thread_config):
        pass

    print("\n--- TEST 2: Verifying Learning (History Survives) ---")
    # Because of SQLite and the Store, Test 2 will automatically use 'Robert'
    inputs2 = {"messages": [HumanMessage(content="Email Bob again.")], "user_id": uid}
    for event in graph.stream(inputs2, thread_config):
        if "assistant" in event:
            print(f"AGENT OUTPUT: {event['assistant']['messages'][0].content}")

if __name__ == "__main__":
    run_milestone_demo()
