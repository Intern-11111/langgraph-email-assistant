from src.tools.tools import is_dangerous_tool

def test_tool():
    assert is_dangerous_tool("send_email")
