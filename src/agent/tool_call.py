from src.tools.calendar import read_calendar
from src.tools.contact import lookup_contact

class ToolExecutorNode:
    """
    Executes tools selected by the reasoning node.
    Tools:
        - read_calendar
        - lookup_contact
        - reply (no tool)
    """

    def execute(self, state: dict) -> dict:
        decision = state.get("reasoning_output", {})
        action = decision.get("action")
        action_input = decision.get("action_input")

        if not action:
            state["tool_result"] = None
            return state

        if action == "read_calendar":
            result = read_calendar(
                user_id="me",
                date_hint=action_input.get("date_hint")
                if isinstance(action_input, dict) else None
            )
            state["tool_result"] = result
            return state

        if action == "lookup_contact":
            query = action_input.get("query", "alice") if isinstance(action_input, dict) else "alice"
            result = lookup_contact(query)
            state["tool_result"] = result
            return state

        if action == "reply":
            state["tool_result"] = {
                "reply": action_input
            }
            return state

        state["tool_result"] = None
        return state

    def __call__(self, state: dict) -> dict:
        return self.execute(state)
