from graph import email_agent_graph
from src.HITL.hitl_graph import build_graph
from langgraph.checkpoint.memory import MemorySaver
"""
Here we run the agent with one email example and see how agent is works and make decision
"""

if __name__ == "__main__":
    state = {
        "email_text": {
            "subject": "schedule today's meeting",
            "body": "Can we schedule a meeting today at 5 pm?",
            "sender": "manager@company.com"
        }
    }

    # final_state = email_agent_graph.invoke(state)

    # print("\nFINAL STATE:")
    # for k, v in final_state.items():
    #     print(f"{k}: {v}")

graph=build_graph()
graph.compile(
        checkpointer=MemorySaver(),
        interrupt_after=["tool"]  
    )


