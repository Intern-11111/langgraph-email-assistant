import json
import time
import uuid
from typing import Any, Dict, List

# Import mock tools
from tools.calendar import read_calendar
from tools.contact import lookup_contact


class ReactAgent:
    def __init__(self, max_steps: int = 6):
        self.max_steps = max_steps

    def _new_trace_id(self) -> str:
        return str(uuid.uuid4())

    def _timestamp(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

    def run(self, email_subject: str, email_body: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run a small ReAct loop for a single email.

        Returns:
            trace dict with keys: trace_id, created_at, input, trace (list of steps), final (summary)
        """
        trace_id = self._new_trace_id()
        created_at = self._timestamp()
        context = context or {}

        # Initial prompt-like internal state
        prompt = f"Subject: {email_subject}\nBody: {email_body}"

        trace: List[Dict[str, Any]] = []

        # Very simple rule to decide initial action:
        # if email mentions 'schedule' or 'meeting' -> try calendar; if includes person name -> lookup contact
        lower_text = (email_subject + " " + email_body).lower()

        # Start loop
        for step in range(1, self.max_steps + 1):
            thought = ""
            action = None
            action_input = None
            observation = None

            # Simple "reasoning" heuristics (toy logic for demo)
            if "schedule" in lower_text or "meeting" in lower_text or "call" in lower_text:
                thought = "Email requests scheduling. I should check the user's calendar and find slots."
                action = "CALL_TOOL"
                action_input = {"tool": "read_calendar", "args": {"user_id": "me", "date_hint": "next available"}}

            elif "who is" in lower_text or "contact" in lower_text or "email" in lower_text:
                thought = "User is asking about a contact. I should look up the contact details."
                action = "CALL_TOOL"
                # attempt to extract a name or token (very naive)
                # If no clear name, use sender from context
                name = context.get("sender") or "alice"
                action_input = {"tool": "lookup_contact", "args": {"query": name}}

            else:
                # If we already called tools once, try to synthesize and finish
                if step > 2:
                    thought = "I have enough context; prepare a final suggested action."
                    action = "FINISH"
                    action_input = {
                        "final_message": "Suggested action: Reply asking for preferred times, propose slots from calendar if available.",
                        "proposed_action": "ask_for_availability"
                    }
                else:
                    thought = "No clear action yet. I'll check calendar proactively to gather context."
                    action = "CALL_TOOL"
                    action_input = {"tool": "read_calendar", "args": {"user_id": "me", "date_hint": None}}

            # Execute action
            if action == "CALL_TOOL":
                tool_name = action_input["tool"]
                args = action_input.get("args", {})
                if tool_name == "read_calendar":
                    observation = read_calendar(**args)
                elif tool_name == "lookup_contact":
                    observation = lookup_contact(**args)
                else:
                    observation = {"tool": tool_name, "error": "Unknown tool"}

                # Optionally update context with observations
                context["last_observation"] = observation
                # Also append available_slots to lower_text so next loop can pick FINISH
                if isinstance(observation, dict) and "available_slots" in observation:
                    lower_text += " calendar_has_slots"

            elif action == "FINISH":
                observation = {"final": action_input}
                # Add final trace and break
                trace.append({
                    "step": step,
                    "timestamp": self._timestamp(),
                    "thought": thought,
                    "action": action,
                    "action_input": action_input,
                    "observation": observation,
                })
                break

            # Append step trace
            trace.append({
                "step": step,
                "timestamp": self._timestamp(),
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation,
            })

        # Summarize final decision
        final_summary = {
            "summary": "Agent suggests follow-up action based on tools and reasoning.",
            "suggested_action": trace[-1]["observation"] if trace else {},
        }

        return {
            "trace_id": trace_id,
            "created_at": created_at,
            "input": {"subject": email_subject, "body": email_body, "context": context},
            "trace": trace,
            "final": final_summary,
        }


if __name__ == "__main__":
    sample_subject = "Schedule a meeting"
    sample_body = "Can we have a Zoom call tomorrow?"
    agent = ReactAgent(max_steps=6)
    result = agent.run(sample_subject, sample_body, context={"sender": "alice"})
    print(json.dumps(result, indent=2))
