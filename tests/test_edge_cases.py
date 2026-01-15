# tests/test_edge_cases.py

import sys
import os

sys.path.append(os.path.abspath("src"))

from hitl_graph import build_hitl_graph

def test_empty_email():
    app = build_hitl_graph()

    result = app.invoke(
        {"email_body": ""},
        config={"configurable": {"thread_id": "edge-empty"}}
    )

    assert result is not None
    print("✅ Empty email handled safely:", result)


def test_ambiguous_email():
    app = build_hitl_graph()

    result = app.invoke(
        {"email_body": "Please do the needful"},
        config={"configurable": {"thread_id": "edge-ambiguous"}}
    )

    assert result is not None
    print("✅ Ambiguous email handled safely:", result)


if __name__ == "__main__":
    test_empty_email()
    test_ambiguous_email()
