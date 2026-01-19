import json
from email_triage.graph import build_graph

app = build_graph()

with open("evaluation/evaluation_dataset.json") as f:
    dataset = json.load(f)

correct = 0

for item in dataset:
    result = app.invoke({"email": item["email"]})
    if result["triage_decision"] == item["label"]:
        correct += 1

total = len(dataset)
accuracy = (correct / total) * 100

print("Total emails tested:", total)
print("Correct predictions:", correct)
print("Accuracy:", accuracy, "%")
