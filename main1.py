from graph import email_agent_graph

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

    final_state = email_agent_graph.invoke(state)

    print("\nFINAL STATE:")
    for k, v in final_state.items():
        print(f"{k}: {v}")



