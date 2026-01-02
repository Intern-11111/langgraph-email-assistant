import json
import time
from typing import Dict, Any, List
from langsmith import traceable

from tools.calendar import read_calendar, create_event
from tools.contact import lookup_contact


SENSITIVE_ACTIONS = {"send_email", "spend_money", "create_event"}


class ReactAgent:
    def __init__(self, max_steps: int = 6):
        self.max_steps = max_steps

    def run(
        self,
        subject: str,
        body: str,
        context: Dict[str, Any] | None = None,
        human_decision: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        # If a sensitive action is detected, the agent PAUSES for human approval.

        trace_steps: List[Dict[str, Any]] = []

        agent_trace = {
            "input": {
                "subject": subject,
                "body": body,
                "context": context or {},
            },
            "trace": trace_steps,
            "final": {},
            "status": "RUNNING",
        }

        # Assign a unique trace id for this run
        agent_trace["trace_id"] = f"trace_{int(time.time())}"

        for step in range(1, self.max_steps + 1):

            # REASONING STEP
            thought = "Analyzing email intent and deciding next action"

            email_text = f"{subject} {body}".lower()

            if "schedule" in email_text or "meeting" in email_text:
                # For demo
                action = "create_event"
                action_input = {
                    "title": "Project Update Meeting",
                    "candidate_times": [
                        "2026-01-03T10:00",
                        "2026-01-03T11:00",
                    ],
                    "attendees": ["manager@company.com"],
                }
            elif "contact" in email_text or "email" in email_text:
                action = "lookup_contact"
                action_input = "manager@company.com"
            else:
                action = "reply"
                action_input = "Thanks for reaching out. I will get back to you shortly."

            # HITL CHECKPOINT (UNDO TEST)
            if action in SENSITIVE_ACTIONS and human_decision is None:
                trace_steps.append({
                    "step": step,
                    "timestamp": time.time(),
                    "thought": thought,
                    "action": action,
                    "action_input": action_input,
                    "observation": None,
                    "paused": True,
                    "reason": "Sensitive action requires human approval",
                })

                agent_trace["status"] = "PAUSED"
                agent_trace["final"] = {
                    "message": "Execution paused for human approval",
                    "pending_action": action,
                    "pending_input": action_input,
                }
                return agent_trace

            #  APPLY HUMAN DECISION (if resuming)
            if human_decision:
                decision = human_decision.get("decision")

                if decision == "deny":
                    trace_steps.append({
                        "step": step,
                        "timestamp": time.time(),
                        "thought": "Human denied the action",
                        "action": "denied",
                        "action_input": action_input,
                        "observation": "Action denied by human",
                    })
                    agent_trace["status"] = "DENIED"
                    agent_trace["final"] = {"status": "denied"}
                    return agent_trace

                elif decision == "edit":
                    action_input = human_decision.get("updated_input", action_input)

                elif decision == "approve":
                    pass  # continue execution normally

            # TOOL EXECUTION
            if action == "read_calendar":
                observation = read_calendar(**action_input)

            elif action == "lookup_contact":
                observation = lookup_contact(action_input)

            elif action == "reply":
                observation = {"reply": action_input}

            elif action == "create_event":
                observation = create_event(action_input)
            else:
                observation = {"error": f"Unknown action: {action}"}

            # TRACE LOGGING
            trace_steps.append({
                "step": step,
                "timestamp": time.time(),
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation,
            })

            # TERMINATION
            if action == "reply":
                agent_trace["status"] = "COMPLETED"
                agent_trace["final"] = {
                    "reply": action_input,
                    "last_observation": observation,
                }
                break

        return agent_trace
    
    def resume(
        self,
        paused_trace: Dict[str, Any],
        human_decision: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Wait for a human decision and resume.

        - Approve: proceeds with tool execution (optionally with updated input).
        - Deny: returns a new trace with status DENIED without executing tools.
        - Edit: prompts for updated input and proceeds.
        """

        if paused_trace.get("status") != "PAUSED":
            raise ValueError("resume() requires a PAUSED trace")

        pending_input = paused_trace["final"]["pending_input"]

        # If no decision provided, interactively prompt the user
        if human_decision is None:
            print("\nPending action:", paused_trace["final"]["pending_action"])
            print("Current input:")
            print(json.dumps(pending_input, indent=2))

            while True:
                raw = input("Enter decision (Approve/Deny/Edit): ").strip().lower()
                if raw in ("approve", "deny", "edit"):
                    decision = raw
                    break
                print("Invalid choice. Please type Approve, Deny, or Edit.")

            if decision == "edit":
                print("Enter updated input as JSON (or blank to keep current):")
                updated_raw = input("> ").strip()
                if updated_raw:
                    try:
                        updated_input = json.loads(updated_raw)
                    except Exception:
                        print("Invalid JSON. Keeping current input.")
                        updated_input = pending_input
                else:
                    updated_input = pending_input
                human_decision = {"decision": "edit", "updated_input": updated_input}
            elif decision == "approve":
                human_decision = {"decision": "approve"}
            else:
                human_decision = {"decision": "deny"}

        # Re-run with the chosen human decision
        return self.run(
            subject=paused_trace["input"]["subject"],
            body=paused_trace["input"]["body"],
            context=paused_trace["input"]["context"],
            human_decision=human_decision,
        )




if __name__ == "__main__":
    agent = ReactAgent(max_steps=3)

    subject = "Team meeting request"
    body = "Can we schedule a meeting for the project update?"

    result = agent.run(subject=subject, body=body, context={"user": "me"})
    print("Initial result:")
    print(json.dumps(result, indent=2))

    if result.get("status") == "PAUSED":
        print("\nAwaiting human decision...")
        resumed = agent.resume(result)
        print("\nResumed result:")
        print(json.dumps(resumed, indent=2))
