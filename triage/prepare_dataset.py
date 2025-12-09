import json
import pandas as pd

# Load JSON dataset
with open("emails_triage.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
label_map = {
    "notify": "notify_human",
    "ignore": "ignore",
    "respond": "respond_act"
}

for item in data:
    text = f"Subject: {item.get('subject', '')}\n\n{item.get('email_thread', '')}"
    orig_label = item["triage"]
    mapped = label_map[orig_label]
    rows.append({
        "id": item["id"],
        "text": text,
        "label": mapped
    })

df = pd.DataFrame(rows)
print(df["label"].value_counts())
df.to_csv("emails_triage.csv", index=False)
print("Saved emails_triage.csv")
