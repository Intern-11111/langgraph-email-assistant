import sys
import os

# Add project root to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from src.hitl_graph import build_hitl_graph

graph = build_hitl_graph()

output = graph.invoke({
    "tool_name": "read_calendar",
    "tool_input": ""
})

print("SAFE TOOL OUTPUT:", output)
