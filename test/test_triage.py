from backend.src.graph import create_graph

workflow = create_graph()

output = workflow.invoke({
    "messages": [],
    "mail": {
        "subject": "Meeting tomorrow?",
        "body": "Hi, can we meet at 3pm tomorrow? Thanks!",
    },
    "tool_name": None,
    "tool_args": None,
    "final_reply": None,
})

config = {"configurable": {"thread_id": "hitl-single-test-v2"}}

output2 = workflow.invoke({
    "messages": [],
    "mail": {
        "subject": "Important Meeting",
        "body": "Hi, can we schedule a meeting for tomorrow at 3 PM? Please send a confirmation." 

    }
})

print("\n=== FINAL STATE ===")
print("triage:", output2["triage_category"])
print("final_reply:", output2.get("final_reply"))
print("===================================================================================================")
print(output2)




