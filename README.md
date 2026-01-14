# langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
<br>
Intelligent ambient agent leveraging LangGraph to process, analyze, and automate email workflows with real-time assistance and proactive insights.

the **"Golden Set"** (Evaluation Dataset) you shared, it appears you want a similar **Test Dataset** tailored specifically for the **Intern-3 Agent Code** I provided earlier. Since the Intern-3 code uses "mock" tools (fake calendar and contacts), your "Golden Set" must match that fake data exactly to be useful for testing. Here is the **Golden Dataset** (Inputs & Reference Outputs) that aligns with the `calendar.py` and `contacts.py` files I wrote for you. ### **1. The Golden Dataset (Visual Table)** This is what your dataset would look like inside LangSmith or a spreadsheet. | **Input (User Prompt)** | **Reference Output (Ideal Answer)** | **Expected Tool Calls** | | --- | --- | --- | | "What is on my calendar for today?" | "You have a **Daily Standup at 09:00 AM** with the team and a **Client Sync at 02:00 PM** with the client." | `read_calendar` | | "Do I have any meetings with the client today?" | "Yes, you have a **Client Sync at 02:00 PM**." | `read_calendar` | | "What is Alice's email address?" | "Alice's email is **alice@company.com** (Project Manager)." | `lookup_contact("Alice")` | | "I need to email Bob. What is his address?" | "Bob's email is **bob@client.com**." | `lookup_contact("Bob")` | | "Check my calendar and find the email for the person I am meeting at 2 PM." | "You are meeting the client at 2 PM. The contact found is Bob, and his email is **bob@client.com**." | `read_calendar`, `lookup_contact` | | "Who is Charlie?" | "I could not find contact details for Charlie." | `lookup_contact("Charlie")` | --- ### **2. The Golden Dataset (Code Format)** To actually use this for evaluation (Milestone 2), you can save this data as a JSON file. **File:** `evaluation_dataset.json` ```json [ { "input": "What is on my calendar for today?", "reference_output": "You have a Daily Standup at 09:00 AM and a Client Sync at 02:00 PM." }, { "input": "What is Alice's email address?", "reference_output": "Alice's email is alice@company.com." }, { "input": "I need to email Bob. What is his address?", "reference_output": "Bob's email is bob@client.com." }, { "input": "Check my calendar and find the email for the person I am meeting at 2 PM.", "reference_output": "The meeting is Client Sync at 02:00 PM with Bob. Bob's email is bob@client.com." }, { "input": "Who is Charlie?", "reference_output": "Contact 'Charlie' was not found." } ] ``` --- ### **3. How to Run an Evaluation (Optional)** If you want to run these tests against your agent immediately (a "Mini Evaluation"), you can use this simple script. It loops through the dataset and checks if the agent returns the expected keywords. **File:** `run_eval.py` ```python import json from agent.react_loop import react_graph from langchain_core.messages import HumanMessage # Load the Golden Dataset with open("evaluation_dataset.json", "r") as f: dataset = json.load(f) print("--- Starting Mini-Evaluation ---") for case in dataset: user_input = case["input"] expected = case["reference_output"] print(f"\nTesting: '{user_input}'") # Run the agent inputs = {"messages": [HumanMessage(content=user_input)]} config = {"configurable": {"thread_id": "eval_run"}} final_response = "" for event in react_graph.stream(inputs, config=config): for value in event.values(): if "messages" in value: last_msg = value["messages"][-1] if last_msg.content: final_response = last_msg.content # Simple Keyword Check (Basic Evaluation) # In LangSmith, an LLM would do this comparison for you. print(f"Agent Output: {final_response}") print(f"Expected: {expected}") ``` ### **Summary of deliverables for this step:** 1. **`evaluation_dataset.json`**: This is your "Golden Set" file. 2. **`run_eval.py`**: A script to run the tests. This will allow you to generate the exact kind of "Inputs vs. Outputs" table shown in your LangSmith screenshot.

# MILESTONE 2 : Ambient Agent 101: Email Assistant Evaluator

This MILESTONE implements an **LLM-as-a-judge** evaluation system using **LangSmith** and **LangChain**. It is designed to automatically score the performance of an ambient AI agent that triages and summarizes corporate emails.

---

## 🚀 Features

* **Dataset Ingestion**: Automatically loads "golden" evaluation data from local JSON files.
* **LLM-as-a-Judge**: Uses `gpt-4o` to perform high-fidelity qualitative scoring of agent outputs.
* **Custom Evaluation Criteria**: Scores responses based on accuracy, conciseness, and tone.
* **Console Reporting**: View real-time scores and judge reasoning directly in your terminal.
* **LangSmith Integration**: Full tracing and experiment history via the LangSmith dashboard.

---

## OUTPUT 
![WhatsApp Image 2026-01-09 at 7 29 49 PM](https://github.com/user-attachments/assets/f6ab41f9-6e76-4209-9c52-fc7b9ce24df4)
