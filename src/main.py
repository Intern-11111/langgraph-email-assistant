import json
import os
import sys
from agents.react_loop import ReactAgent
from tools.calendar import read_calendar
from tools.contact import lookup_contact
from utils.excel_exporter import export_outputs_to_excel


def main():
    # Support running without args by using a friendly default
    if len(sys.argv) < 3:
        subject = "Meeting request"
        body = "Can we schedule for tomorrow?"
        print("No arguments provided. Using default subject/body.")
        print("Usage: python src/main.py \"Subject\" \"Body\"")
    else:
        subject = sys.argv[1]
        body = sys.argv[2]

    agent = ReactAgent(max_steps=6)
    trace = agent.run(subject, body, context={"sender": "manager@company.com"})

    print(json.dumps(trace, indent=2))

    # Optional Excel export (interactive prompt)
    try:
        default_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "agent_outputs.xlsx")
        choice = input("\nExport outputs to Excel? (y=save to default, c=choose path, N=skip) [y/N/c]: ").strip().lower()
        if choice in ("y", "yes"):
            out_path = default_out
        elif choice in ("c", "choose", "custom"):
            out_path = input(f"Enter Excel output path [{default_out}]: ").strip() or default_out
        else:
            out_path = None

        if out_path:
            # Gather tool outputs for inclusion
            cal = read_calendar(user_id="me", date_hint="next available")
            # Try to lookup a useful contact based on sender
            contact = lookup_contact("manager@company.com")
            export_outputs_to_excel(out_path, agent_trace=trace, calendar_output=cal, contact_output=contact)
            print(f"\nExcel results saved to: {out_path}")
    except Exception as e:
        print("\nExcel export failed:", e)


if __name__ == "__main__":
    main()
