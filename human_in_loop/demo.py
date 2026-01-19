from dotenv import load_dotenv
load_dotenv()

from langsmith import traceable
from human_in_loop.graph import build_graph

def run_demo():
    graph = build_graph()

    emails = [
        "Please unsubscribe me from this promotion",
        "Can we schedule a meeting tomorrow?",
        "Urgent! Your bank account needs verification"
    ]

    for email in emails:
        print("\n==============================")
        print("Processing Email:", email)

        state = {
            "email": email,
            "triage_decision": "",
            "reasoning": "",
            "human_decision": None
        }

        # 🔑 IMPORTANT: capture returned state
        final_state = graph.invoke(state)

        print("Final Output:", {
            "email": final_state["email"],
            "ai_decision": final_state["triage_decision"],
            "human_decision": final_state["human_decision"]
        })

if __name__ == "__main__":
    run_demo()
