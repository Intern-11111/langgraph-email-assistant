# milestone_4_tool_interrupt/demo.py

from .graph import build_graph

emails = [
    "Please unsubscribe me from this promotion",
    "Can we schedule a meeting tomorrow?",
    "Urgent! Your bank account needs verification"
]

def run_demo():
    app = build_graph()

    for email in emails:
        print("\n==============================")
        print("Processing Email:", email)

        state = {
            "email": email
        }

        result = app.invoke(state)

        # Final result after interrupt
        if result.get("approved") is True:
            print("✅ Final Decision: Tool approved by human")
        elif result.get("approved") is False:
            print("❌ Final Decision: Tool denied by human")
        else:
            print("ℹ️ No unsafe action detected")

if __name__ == "__main__":
    run_demo()
