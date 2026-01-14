# langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
<br>
Intelligent ambient agent leveraging LangGraph to process, analyze, and automate email workflows with real-time assistance and proactive insights.
<br>
##----- MILESTONE 1 -----
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

###Step 2: Set up the Python environment

Make sure you have Python 3.9+ installed.

Create the project folder, e.g.:

Windows: C:\email_triage_project

macOS/Linux: ~/email_triage_project


Open a terminal in that folder:

Windows: open the folder in Explorer → click address bar → type cmd → Enter.

macOS/Linux: cd ~/email_triage_project.

nstall dependencies:  pip install "transformers>=4.45.0" "datasets>=3.0.0" "accelerate" "scikit-learn" pandas

###Step 3: Convert JSON dataset → training CSV

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


###Step 4: Train the triage classifier (transformer fine‑tuning)

The classifier is a small transformer (e.g., distilbert-base-uncased) fine‑tuned for 3‑way intent classification on your dataset. This follows a common pattern for email intent/triage models.
​
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



###Step 5: Implement the Triage Node (rules + model)

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

##---- MILESTONE 2 ----

This milestone implements an LLM-as-a-Judge framework to evaluate AI Agents using custom metrics and structured grading rubrics. Instead of relying on generic benchmarks, this system uses a dedicated "Judge" model to provide granular feedback on agent performance. 

Key Features
-Custom Quality Metrics: Automated scoring for Helpfulness, Tone, and Accuracy.

-Structured Grading: Uses Pydantic to ensure the Judge always returns valid JSON.

-Provider Agnostic: Easily switch between OpenAI (GPT-4o) and Google (Gemini).

-Reasoning-First: The judge doesn't just give a number; it provides an explanation for every score.

Prerequisites:
pip install langchain-openai langchain-google-genai python-dotenv pydantic

Configuration:
OPENAI_API_KEY=your_key_here  --> in env file

Final output got in this milestone ::

valuate.py

--- OpenAI Quality Report ---

Helpfulness: 5/5

Tone:        5/5

Accuracy:    5/5

Result:      PASS

Reasoning:   The response effectively addresses the user's request for a refund, provides a clear action taken (initiating the refund), and gives a reasonable timeframe for when the user can expect the refund. The tone is empathetic and professional, acknowledging the user's frustration without being dismissive. All criteria are met excellently, leading to a perfect score.

##-- MILESTONE 3--

This milestone focuses on modifying an autonomous email agent from a stateless execution model to a stateful, resilient system. By integrating a relational database (SQLite) for state persistence and implementing a Human-In-The-Loop (HITL) checkpoint.


The files added in the folder are: state.py, node.py, graph.py and test_persistence.py

-state.py define: The AgentState using TypedDict. It utilizes Annotated with the add_messages reducer to ensure that conversation history is preserved as a cumulative list rather than being overwritten.

-node.py: Contains the functional units of the graph: 1)Triage Node: Categorizes incoming emails. 2)React Model Node: Generates draft responses. 3)Action Node: Executes the high-stakes side-effect (sending the email).

-graph.py: The core logic where the workflow is compiled. It integrates the SqliteSaver checkpointer and enforces the interrupt_before protocol on the action_node.


Persistence Layer

It implemented SqliteSaver to serve as the checkpointer. This translates the ephemeral Python state into a binary format stored in checkpoints.sqlite.

Thread Identification: Every session is tracked via a thread_id. This allows the agent to distinguish between multiple concurrent users and retrieve the correct memory from the database.


Human-In-The-Loop (HITL) Checkpoint

The graph is configured to halt execution immediately before the action_node.

Safety Protocol: By using interrupt_before=["action_node"], the system ensures that no email is dispatched without explicit human verification.

State Suspension: Upon interruption, the current state is serialized to the database, allowing the program to exit without data loss.

Demonstration of Milestone (Fail/Recover Test):

To prove the efficacy of the persistence layer, test_persistence.py) that executes the following lifecycle: 1)Stage 1 (State Injection): The agent processes an email and reaches the interrupt. The program "finishes" execution, but the state remains in the database. 2)Simulation of Latency: A simulated delay represents the time taken for human review. 3)Stage 2 (Re-hydration): The script is triggered again. It fetches the state from the checkpoints.sqlite using the thread_id, realizes it is at a checkpoint, and resumes to complete the action without needing the original input again.

Dependencies & Installation: pip install langgraph-checkpoint-sqlite

output acheived in this milestone :

Checkpointer loaded successfully!

---Stage 1: INITIAL PROCESSING ---

--- TRIAGING EMAIL ---

Current Node: triage_node

--- AGENT IS THINKING ---

Current Node: react_model

Current Node: __interrupt__


SYSTEM PAUSED: HITL Interrupt triggered.

Verification: Check your folder for 'checkpoints.sqlite'.

The agent is now 'asleep' in the database.

Simulating system wait... 3

Simulating system wait... 2

Simulating system wait... 1

--- STAGE 2: RECOVERING FROM DATABASE ---
Resuming based on thread_id...
--- EXECUTING TOOLS (ACTION) ---
Resumed Node: react_tools
--- AGENT IS THINKING ---
Resumed Node: react_model
Resumed Node: __interrupt__

# Milestone 4: Persistent Memory & Ambient Learning

### 1. Overview
Milestone 4 marks the final phase of the Email Assistant project. The focus shifts from a stateless reactive agent to a **Stateful Ambient Agent**. This implementation achieves "True Autonomy" by integrating a persistent SQLite database for session history and a Long-Term Store for user preference adaptation.



---

### 2. Milestone 4 Requirement Checklist
This implementation satisfies the following mentor-specified requirements:

- [x] **REQ 1: MemorySaver Implementation** – Integrated `SqliteSaver` to persist the graph state.
- [x] **REQ 2: Thread Management** – Implemented `thread_id` logic to isolate and recall user sessions.
- [x] **REQ 3: Compile with Checkpointer** – Graph is compiled with `checkpointer=sqlite`.
- [x] **REQ 4: History Survival** – Messages and state are stored in `m4.db`, surviving script restarts.
- [x] **REQ 5: Flag Unsafe Tools** – Automated routing to an interrupt node for "sensitive" actions (Email drafting).
- [x] **REQ 6: Configure Interrupts** – Utilizes the LangGraph `interrupt()` function to pause execution.
- [x] **REQ 7: Notify User** – Interactive console alerts notify the user when the agent requires input.
- [x] **REQ 8: Learning & Deliverable** – The agent successfully adapts to human feedback (e.g., learning a name change) via the `BaseStore`.

---

### 3. System Architecture
The agent utilizes a **Dual-Layer Memory Architecture** to achieve learning:

1. **Short-Term Memory (Checkpointing):** Uses SQLite to store the current conversation thread. If the application crashes, the agent resumes exactly where it left off.
2. **Long-Term Memory (The Store):** Uses an `InMemoryStore` to "distill" human feedback. This allows the agent to learn preferences that persist across different threads.



---

### 4. Technical Approach: "Persistent Simulation"
To ensure the project remains fully executable without external API dependencies (OpenAI Rate Limits or Google Cloud Credentials), this version utilizes **Mock Reasoning Nodes**. 

- **The Logic:** The nodes follow the exact LangGraph library standards for state management and HITL interrupts. 
- **The Learning:** Instead of a live LLM call, the reasoning node queries the `BaseStore`. If it finds a stored correction (e.g., *"His name is Robert"*), it automatically overrides the default output to reflect the learned information.

---

#### Running the Demo
python mfour.py 

### output in this milestone :
<img width="978" height="558" alt="image" src="https://github.com/user-attachments/assets/8f749483-13dc-47b1-ae5f-9e0c0c595870" />

