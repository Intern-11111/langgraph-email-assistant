import sys
import os
import uuid

# ✅ Add project folder to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.react_loop import build_graph

if __name__ == "__main__":

    app = build_graph()

    while True:
        user_input = input("\nAsk something (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        input_state = {
            "query": user_input,
            "thoughts": [],
            "action": "",
            "observation": "",
            "trace_id": str(uuid.uuid4()),
            "result": ""
        }

        result = app.invoke(input_state)

        print("\nAgent Response")
        print(result["result"])
