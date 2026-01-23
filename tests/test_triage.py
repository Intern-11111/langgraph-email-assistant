from src.triage.triage_node import triage_node


def test_triage_urgent_email():
    state = {
        "email": {
            "subject": "Urgent meeting",
            "body": "Please attend"
        }
    }

    result = triage_node(state)
    assert result["triage_decision"] == "respond"


def test_triage_non_urgent_email():
    state = {
        "email": {
            "subject": "Hello",
            "body": "Just checking in"
        }
    }

    result = triage_node(state)
    assert result["triage_decision"] == "needs_human_review"
