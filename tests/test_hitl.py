from src.react_agent.approval import approval_node


def test_pause_without_user_action():
    state = {
        "draft_response": "Draft message"
    }

    result = approval_node(state)
    assert result["paused"] is True


def test_approve_action():
    state = {
        "draft_response": "Draft message"
    }

    result = approval_node(state, user_action="approve")
    assert result["paused"] is False
    assert result["approved"] is True
