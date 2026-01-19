from .graph import build_graph


emails = [
    "Please unsubscribe me from this promotion",
    "Can we schedule a meeting tomorrow?",
    "Urgent! Your bank account needs verification"
]

app = build_graph()

for email in emails:
    print("\n==============================")
    print("Input Email:", email)
    result = app.invoke({"email": email})
    print("Triage Decision:", result["triage_decision"])
    print("Reasoning:", result["reasoning"])
