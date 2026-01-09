import json
import os
import time
import argparse
from datetime import datetime
from typing import Dict, Any, List
from langsmith import traceable

from tools.calendar import read_calendar, create_event
from tools.contact import lookup_contact
from triage.triage_rules import TriageRules


SENSITIVE_ACTIONS = {"send_email", "spend_money", "create_event"}


def is_sensitive_action(action: str) -> bool:
    return action in SENSITIVE_ACTIONS


def decide_action(subject: str, body: str) -> tuple[str, Any]:
    email_text = f"{subject} {body}".lower()

    if "schedule" in email_text or "meeting" in email_text:
        return (
            "create_event",
            {
                "title": "Project Update Meeting",
                "candidate_times": [
                    "2026-01-03T10:00",
                    "2026-01-03T11:00",
                ],
                "attendees": ["manager@company.com"],
            },
        )
    elif "contact" in email_text or "email" in email_text:
        return "lookup_contact", "manager@company.com"
    else:
        return "reply", "Thanks for reaching out. I will get back to you shortly."


def is_malicious_email(subject: str, body: str, sender: str | None = None) -> dict | None:
    """
    Returns a dict with reason if the email looks malicious/spam/urgent-payment/scam; otherwise None.
    Uses rule-based triage plus extra urgency/scam heuristics.
    """
    triage = TriageRules()
    res = triage.classify(subject, body, sender or "")
    label = res.get("label")
    confidence = float(res.get("confidence", 0.0))

    text = f"{subject} {body}".lower()

    urgent_terms = [
        "urgent", "immediately", "asap", "right away", "act now", "overdue",
        "final notice", "last warning", "past due", "pay now",
    ]
    scam_terms = [
        "gift card", "wire transfer", "crypto", "bitcoin", "ethereum",
        "bank account details", "routing number", "verification code", "otp",
        "click this link to verify", "reset your password now",
    ]
    payment_terms = [
        "payment", "invoice", "bill", "fee", "transfer", "payable",
    ]

    has_urgent = any(t in text for t in urgent_terms)
    has_scam = any(t in text for t in scam_terms)
    has_payment = any(t in text for t in payment_terms)

    # Primary rule-based deny
    if label == "spam" and confidence >= 0.6:
        return {"reason": "Detected spam email", "category": label, "confidence": confidence}

    # Finance-related with urgency/scam signals
    if label == "finance" and (has_urgent or has_scam) and confidence >= 0.6:
        return {
            "reason": "Urgent finance/payment request looks risky",
            "category": label,
            "confidence": confidence,
        }

    # Generic scam/urgency combination even if label uncertain
    if has_scam or (has_payment and has_urgent):
        return {
            "reason": "Suspicious payment urgency or scam indicators",
            "category": label or "heuristic",
            "confidence": max(confidence, 0.6),
        }

    return None


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

        # spam/payment urgency/scam detection
        mal = is_malicious_email(subject, body, (context or {}).get("sender"))
        if mal is not None and human_decision is None:
            trace_steps.append({
                "step": 0,
                "timestamp": time.time(),
                "thought": "Pre-check for malicious/spam email",
                "action": "auto_deny",
                "action_input": {"subject": subject, "body": body},
                "observation": mal,
            })
            agent_trace["status"] = "DENIED"
            agent_trace["final"] = {
                "status": "denied",
                "reason": mal.get("reason"),
                "category": mal.get("category"),
                "confidence": mal.get("confidence"),
            }
            return agent_trace

        for step in range(1, self.max_steps + 1):

            # REASONING STEP
            thought = "Analyzing email intent and deciding next action"
            action, action_input = decide_action(subject, body)

            # HITL CHECKPOINT (UNDO TEST)
            if is_sensitive_action(action) and human_decision is None:
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
                agent_trace["status"] = "Approved"
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
        Pauses for a human decision and resume.

        - Approve: proceeds with tool execution (optionally with updated input).
        - Deny: returns a new trace with status DENIED without executing tools.
        - Edit: prompts for updated input and proceeds.
        """

        if paused_trace.get("status") != "PAUSED":
            raise ValueError("resume() requires a PAUSED trace")

        pending_input = paused_trace["final"]["pending_input"]
        pending_action = paused_trace["final"].get("pending_action")

        def _input_nonempty(prompt: str, default: str | None = None) -> str | None:
            val = input(prompt).strip()
            if not val and default is not None:
                return default
            return val if val else None

        def _parse_csv_list(raw: str) -> List[str]:
            return [x.strip() for x in raw.split(",") if x.strip()]

        def _guided_edit(action: str, data: Any) -> Any:
            #Just return original if guided edit isn't applicable
            if action == "create_event" and isinstance(data, dict):
                print("\nGuided editor: create_event")
                print("Current event:")
                try:
                    print(json.dumps(data, indent=2))
                except Exception:
                    print(str(data))

                # Title
                current_title = data.get("title")
                new_title = _input_nonempty(f"Title [{current_title}]: ", default=current_title)
                if new_title is not None:
                    data["title"] = new_title

                # Candidate times
                current_times = data.get("candidate_times")
                if not isinstance(current_times, list):
                    current_times = []
                print("Current candidate_times:", current_times)
                times_raw = _input_nonempty(
                    "Candidate times (comma-separated ISO; blank to keep): ",
                    default=None,
                )
                if times_raw is not None:
                    data["candidate_times"] = _parse_csv_list(times_raw)

                # Attendees
                current_attendees = data.get("attendees")
                if not isinstance(current_attendees, list):
                    current_attendees = []
                print("Current attendees:", current_attendees)
                attendees_raw = _input_nonempty(
                    "Attendees (comma-separated emails; blank to keep): ",
                    default=None,
                )
                if attendees_raw is not None:
                    data["attendees"] = _parse_csv_list(attendees_raw)

                return data
            elif action == "reply":
                print("\nGuided editor: reply")
                print("Current reply:")
                try:
                    print(json.dumps(data, indent=2))
                except Exception:
                    print(str(data))
                new_reply = _input_nonempty("Reply text [leave blank to keep]: ", default=None)
                if isinstance(data, dict):
                    if new_reply is not None:
                        data["reply"] = new_reply
                    return data
                # If reply is raw string
                return new_reply if new_reply is not None else data
            else:
                # Generic JSON edit fallback
                print("\nEnter updated input as JSON (blank to keep current):")
                updated_raw = input("> ").strip()
                if updated_raw:
                    try:
                        return json.loads(updated_raw)
                    except Exception:
                        print("Invalid JSON. Keeping current input.")
                        return data
                return data

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
                # Guided editing flow
                updated_input = _guided_edit(pending_action, pending_input)
                human_decision = {"decision": "edit", "updated_input": updated_input}
            elif decision == "approve":
                human_decision = {"decision": "approve"}
            else:
                human_decision = {"decision": "deny"}
        else:
            if (
                human_decision.get("decision") == "edit"
                and "updated_input" not in human_decision
            ):
                updated_input = _guided_edit(pending_action, pending_input)
                human_decision["updated_input"] = updated_input

        # Re-run with the chosen human decision
        return self.run(
            subject=paused_trace["input"]["subject"],
            body=paused_trace["input"]["body"],
            context=paused_trace["input"]["context"],
            human_decision=human_decision,
        )




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check mail status via ReactAgent")
    parser.add_argument("--subject", required=True, help="Email subject text")
    parser.add_argument("--body", required=True, help="Email body text")
    parser.add_argument(
        "--decision",
        choices=["approve", "deny", "edit"],
        help="Optional human decision to apply if run pauses",
    )
    parser.add_argument(
        "--updated-input",
        help="JSON string for updated input when --decision edit is used",
    )
    parser.add_argument(
        "--save-path",
        default=os.path.join("data", "cli_mail_inputs.json"),
        help="Path to JSON file where CLI inputs will be saved",
    )
    args = parser.parse_args()

    def _ensure_dir(path: str) -> None:
        directory = os.path.dirname(os.path.abspath(path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def save_cli_input(save_path: str, entry: Dict[str, Any]) -> None:
        _ensure_dir(save_path)
        data: List[Dict[str, Any]] = []
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except Exception:
                # If file is corrupt or empty, start a new list
                data = []
        data.append(entry)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # update existing records in user_events.json after an edit
    def _load_events(path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save_events(path: str, events: List[Dict[str, Any]]) -> None:
        _ensure_dir(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2, ensure_ascii=False)

    def _update_last_record(store_path: str, tool: str, update: Dict[str, Any]) -> bool:
        """
        - For create_event: merge into record['event']
        - For email_status: merge top-level keys and nested 'final' if provided

        Returns True if an update was applied.
        """
        events = _load_events(store_path)
        if not events:
            return False
        # find last index with matching tool
        target_idx = None
        for i in range(len(events) - 1, -1, -1):
            if events[i].get("tool") == tool:
                target_idx = i
                break
        if target_idx is None:
            return False
        rec = events[target_idx]
        if tool == "create_event":
            ev = rec.get("event", {})
            if not isinstance(ev, dict):
                ev = {}
            ev.update(update or {})
            rec["event"] = ev
        elif tool == "email_status":
            for k, v in (update or {}).items():
                if k == "final" and isinstance(v, dict):
                    final = rec.get("final", {})
                    if not isinstance(final, dict):
                        final = {}
                    final.update(v)
                    rec["final"] = final
                else:
                    rec[k] = v
        else:
            # fallback shallow merge
            for k, v in (update or {}).items():
                rec[k] = v
        events[target_idx] = rec
        _save_events(store_path, events)
        return True

    # Build the CLI input entry and persist it
    cli_entry: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "subject": args.subject,
        "body": args.body,
        "decision": args.decision,
    }
    if args.decision == "edit" and args.updated_input:
        try:
            cli_entry["updated_input"] = json.loads(args.updated_input)
        except Exception:
            cli_entry["updated_input"] = {
                "_parse_error": "Invalid JSON provided in --updated-input",
                "raw": args.updated_input,
            }
    save_cli_input(args.save_path, cli_entry)

    # Execute the agent and report status
    agent = ReactAgent(max_steps=3)
    result = agent.run(subject=args.subject, body=args.body, context={"source": "cli"})

    print("Status:", result.get("status"))
    print("Trace ID:", result.get("trace_id"))

    # Helper to save final output into user events log
    def save_output_event(final_result: Dict[str, Any]) -> None:
        store_path = os.path.join("data", "user_events.json")
        _ensure_dir(store_path)
        record = {
            "tool": "email_status",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input": {"subject": args.subject, "body": args.body},
            "status": final_result.get("status"),
            "trace_id": final_result.get("trace_id"),
            "final": final_result.get("final"),
        }
        existing: List[Dict[str, Any]] = []
        if os.path.exists(store_path):
            try:
                with open(store_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = []
            except Exception:
                existing = []
        existing.append(record)
        with open(store_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

    # If paused, either apply provided decision or prompt interactively
    if result.get("status") == "PAUSED":
        if args.decision:
            human_decision: Dict[str, Any] = {"decision": args.decision}
            if args.decision == "edit" and args.updated_input:
                try:
                    human_decision["updated_input"] = json.loads(args.updated_input)
                except Exception:
                    pass  # already captured in saved CLI entry; proceed without updating
            resumed = agent.resume(result, human_decision=human_decision)
        else:
            print("\nAwaiting human decision...")
            resumed = agent.resume(result)  # interactive prompt

        print("Resumed Status:", resumed.get("status"))
        print(json.dumps(resumed, indent=2))
        # Save final output to user_events.json
        save_output_event(resumed)
        # If this was an edit, update the relevant existing record in-place
        if args.decision == "edit":
            try:
                pending_action = result.get("final", {}).get("pending_action")
                store_path = os.path.join("data", "user_events.json")
                # Prefer the actual action_input used during resumed run
                last_action_input = None
                if isinstance(resumed.get("trace"), list):
                    for frame in reversed(resumed["trace"]):
                        if frame.get("action") == pending_action:
                            last_action_input = frame.get("action_input")
                            break
                if pending_action == "create_event" and isinstance(last_action_input, dict):
                    applied = _update_last_record(store_path, "create_event", last_action_input)
                    if applied:
                        print("Updated last create_event record with edited input.")
                elif pending_action == "reply" and isinstance(last_action_input, dict):
                    applied = _update_last_record(store_path, "email_status", {"final": last_action_input})
                    if applied:
                        print("Updated last email_status record with edited reply.")
            except Exception as _:
                #  keep going even if update fails
                pass
    else:
        print(json.dumps(result, indent=2))
        save_output_event(result)
