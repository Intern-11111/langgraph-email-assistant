from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.triage_node import triage_email
from agent.react_loop import react_agent

def end_node(state):
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("triage", triage_email)
    graph.add_node("react", react_agent)
    graph.add_node("end", end_node)

    graph.set_entry_point("triage")

    graph.add_conditional_edges(
        "triage",
        lambda state: state["triage_decision"],
        {
            "ignore": "end",
            "notify_human": "end",
            "respond": "react",
        },
    )

    graph.set_finish_point("end")

    return graph.compile()


if __name__ == "__main__":
    # email = {
    #     "subject": "Meeting request",
    #     "email_body": "Can we schedule a meeting tomorrow?"
    # }
    # email = {
    # "subject": "Sale",
    # "email_body": "Huge discount sale today! Unsubscribe here"
    # }
    email = {
    "subject": "Complaint",
    "email_body": "I have a serious complaint about your service"
    }


    app = build_graph()
    result = app.invoke({"email": email})

    print("TRIAGE:", result["triage_decision"])
    print("REPLY:", result.get("agent_reply"))
