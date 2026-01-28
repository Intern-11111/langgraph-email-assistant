# evaluate_milestone2.py
from graph import build_graph
from data.email_test_dataset import TEST_EMAILS

app = build_graph()

correct = 0
total = len(TEST_EMAILS)

for idx, test in enumerate(TEST_EMAILS, start=1):
    result = app.invoke(
        {
            "sender": "",
            "subject": test["subject"],
            "body": test["body"],
            "category": None,
            "intent": None,
            "requires_approval": False,
            "approved": None,
            "action_taken": None
        },
        config={
            "configurable": {
                "thread_id": f"eval_{idx}"
            }
        }
    )

    predicted = result["category"]
    expected = test["expected_category"]

    print(f"[{idx}] Expected: {expected} | Predicted: {predicted}")

    if predicted == expected:
        correct += 1

accuracy = (correct / total) * 100
print("\n📊 Triage Accuracy:", accuracy, "%")
