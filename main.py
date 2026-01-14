import os
import uuid
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from agent.react_loop import react_graph

# Load environment variables (API keys)
load_dotenv()

# Define unsafe tools that require human approval
UNSAFE_TOOLS = {"send_email", "delete_file", "post_to_slack"}


def run_cli():
    print("--- Ambient Agent: Intern-3 Deliverable (ReAct Loop) ---")
    print("Type 'quit' to exit.\n")

    # Generate a unique thread_id (session memory)
    trace_id = str(uuid.uuid4())
    print(f"Session Trace ID: {trace_id}\n")

    config = {
        "configurable": {
            "thread_id": trace_id
        }
    }

    while True:
        user_input = input("User: ")

        if user_input.lower() in {"quit", "exit"}:
            print("Exiting session...")
            break

        inputs = {
            "messages": [HumanMessage(content=user_input)]
        }

        print("\n--- Agent Reasoning Trace ---")

        for event in react_graph.stream(inputs, config=config):
            for value in event.values():
                if "messages" not in value:
                    continue

                last_msg = value["messages"][-1]

                # === TOOL DECISION (Act) ===
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    print("\n[DECISION]: Agent wants to call tool(s):")

                    for tc in last_msg.tool_calls:
                        tool_name = tc["name"]
                        print(f" - Tool: {tool_name}")
                        print(f" - Args: {tc['args']}")

                        # 🚨 Unsafe tool handling
                        if tool_name in UNSAFE_TOOLS:
                            print("\n🚨 [INTERRUPT]: Unsafe tool detected!")
                            print("⚠️ This action requires human approval.")
                            approval = input("Approve tool execution? (yes/no): ")

                            if approval.lower() != "yes":
                                print("❌ Tool execution cancelled by user.")
                                return

                            print("✅ Tool execution approved. Resuming agent...")

                # === TOOL OBSERVATION ===
                elif last_msg.type == "tool":
                    print("\n[OBSERVATION]: Tool returned data:")
                    print(f" {last_msg.content}")

                # === FINAL RESPONSE ===
                elif last_msg.content:
                    print("\n[RESPONSE]:")
                    print(last_msg.content)

        print("\n-----------------------------\n")


if __name__ == "__main__":
    run_cli()
