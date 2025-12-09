# langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
<br>
Intelligent ambient agent leveraging LangGraph to process, analyze, and automate email workflows with real-time assistance and proactive insights.
<br>

##Buiding The Triage Node.
The goal is to automatically decide what to do with each email:
1.ignore: bulk newsletters, promos, social updates, low‑value digests.
2.notify_human: informational updates the user should see, but doesn’t need to reply to
3.respond_act: emails that clearly require a reply or action (decisions, approvals, scheduling, data requests).

The project is structured as a small ML pipeline plus a “triage node” function:
1.Curate and store a balanced labeled dataset.
2.Convert it into a training‑ready CSV.
3.Fine‑tune a transformer classifier on the triage task.
4.Wrap the trained model (plus simple rules) in a function suitable for use in an agent/workflow.

structure and info about files in triage folder:
1.emails_triage.json – Labeled golden dataset (48 emails).
2.emails_triage.csv – Derived CSV with text + labels (generated).
3.prepare_dataset.py – Script to build the CSV from the JSON.
4.train_model.py – Script to fine‑tune the triage classifier.
5.triage_model – Saved trained model and tokenizer (generated).
6.triage_node.py – Triage node: loads the model, applies rules + model to classify new emails.

Step 1: Create a balanced “golden” dataset
Start from a set of realistic corporate‑style emails, covering:
System notifications (deployments, backups, incidents, policy updates).
HR/finance/compliance updates.
Pure marketing / promo / social notifications.
Explicit requests (approvals, scheduling, technical questions, external inquiries).

Label each email with:
notify (will be mapped to notify_human), ignore, respond (will be mapped to respond_act).
Select a balanced subset:
16 emails labeled notify.
16 emails labeled ignore.
16 emails labeled respond.
Total: 48 emails.

Save this as a single JSON array named emails_triage.json in the project folder.
Each item has fields like:
"id" – unique identifier (e.g., email_notify_001),
"author", "to", "subject",
"email_thread" – multi‑line email body,
"triage" – notify / ignore / respond,
"response_summary" – natural‑language explanation of the appropriate human action.

This dataset is your golden set for both training and evaluating the behavior of the triage node.​

Step 2: Set up the Python environment
Make sure you have Python 3.9+ installed.
Create the project folder, e.g.:
Windows: C:\email_triage_project
macOS/Linux: ~/email_triage_project

Open a terminal in that folder:
Windows: open the folder in Explorer → click address bar → type cmd → Enter.
macOS/Linux: cd ~/email_triage_project.

nstall dependencies:  pip install "transformers>=4.45.0" "datasets>=3.0.0" "accelerate" "scikit-learn" pandas

Step 3: Convert JSON dataset → training CSV
The model will be trained on “subject + body” text and a mapped label. To prepare that:
Create prepare_dataset.py in the project folder.

The script:
Loads emails_triage.json.
Concatenates subject + email_thread into a single text field.

Maps:
notify → notify_human
ignore → ignore
respond → respond_act
Writes emails_triage.csv with columns: id, text, label.
Run i command prompt : python prepare_dataset.py
You now have emails_triage.csv, a simple supervised dataset suitable for training a text classifier.

Step 4: Train the triage classifier (transformer fine‑tuning)
The classifier is a small transformer (e.g., distilbert-base-uncased) fine‑tuned for 3‑way intent classification on your dataset. This follows a common pattern for email intent/triage models.​
Create train_model.py in the project folder.
The script does the following:
Loads emails_triage.csv.
Maps labels to IDs: ignore → 0, notify_human → 1, respond_act → 2.
Creates a train/validation split (e.g., 75/25) stratified by label.
Uses Hugging Face datasets + transformers to tokenize text and fine‑tune the model.
Tracks accuracy and macro‑F1.
Saves the best model and tokenizer to ./triage_model.
Run : python train_model.py
This will download the base model, fine‑tune it, and create a triage_model/ directory containing:
config.json, pytorch_model.bin, etc. (model weights and config)
tokenizer files
This is the packaged classifier used by the triage node

Step 5: Implement the Triage Node (rules + model)
The triage node is a Python module that:
Loads the fine‑tuned model and tokenizer.
Defines a function that:
Accepts an email dict (id, subject, from, body).
Optionally applies some simple rule‑based overrides.
Uses the model to predict one of the 3 classes.
Returns a JSON‑like dict containing id, triage, confidence, and a human‑readable reason.
This mirrors how many production email‑triage setups combine rules and ML for robustness.

Rule‑based overrides + safety defaults
Add a thin rule layer in triage_node.py to handle obvious promo/status cases and protect against low‑confidence “ignore” mistakes:
Run : python triage_node.py

Output :
{'id': 'test_001', 'triage': 'respond_act', 'confidence': 0.9322366118431091, 'reason': 'Email contains an explicit request for information, approval, or scheduling.'}



