import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# 1) Load CSV
df = pd.read_csv("emails_triage.csv")

label2id = {"ignore": 0, "notify_human": 1, "respond_act": 2}
id2label = {v: k for k, v in label2id.items()}
df["label_id"] = df["label"].map(label2id)

train_df, val_df = train_test_split(
    df,
    test_size=0.25,
    stratify=df["label_id"],
    random_state=42
)

train_ds = Dataset.from_pandas(train_df)
val_ds = Dataset.from_pandas(val_df)

# 2) Tokenizer & model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_fn(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=256
    )

train_ds = train_ds.map(tokenize_fn, batched=True)
val_ds   = val_ds.map(tokenize_fn, batched=True)

cols_to_keep = ["input_ids", "attention_mask", "label_id"]
train_ds = train_ds.remove_columns([c for c in train_ds.column_names if c not in cols_to_keep])
val_ds   = val_ds.remove_columns([c for c in val_ds.column_names if c not in cols_to_keep])
train_ds = train_ds.rename_column("label_id", "labels")
val_ds   = val_ds.rename_column("label_id", "labels")
train_ds.set_format("torch")
val_ds.set_format("torch")

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3,
    id2label=id2label,
    label2id=label2id
)

def compute_metrics(pred):
    logits, labels = pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average="macro")
    }

training_args = TrainingArguments(
    output_dir="./triage_model",
    num_train_epochs=10,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    learning_rate=5e-5,
    eval_strategy="epoch",  
    save_strategy="epoch",        # <- changed name
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro",
    logging_steps=5,
    save_total_limit=1,
    seed=42
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model("./triage_model")
tokenizer.save_pretrained("./triage_model")
print("Model saved to ./triage_model")
