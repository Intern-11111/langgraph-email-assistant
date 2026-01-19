from datetime import datetime
from shared.memory import load_memory, save_memory

def pause_for_human(state):
    email = state["email"]
    decision = state["triage_decision"]

    memory = load_memory()

    # 🔁 AUTO-REUSE MEMORY
    if email in memory:
        print("\n--- MEMORY HIT ---")
        print("Using stored human preference")
        state["human_decision"] = memory[email]
        return state

    print("\n--- PAUSE STATE ---")
    print("Email:", email)
    print("AI Decision:", decision)
    print("Reasoning:", state["reasoning"])

    if decision == "ignore":
        print("\nOnly approval is allowed for ignored emails.")
        state["human_decision"] = "approve"

    elif decision == "notify_human":
        print("\nChoose one option:")
        print("1. approve")
        print("2. deny")
        choice = input("Your choice: ").strip()
        state["human_decision"] = "approve" if choice == "1" else "deny"

    else:  # respond
        print("\nChoose one option:")
        print("1. approve")
        print("2. deny")
        print("3. edit")

        choice = input("Your choice: ").strip()

        if choice == "3":
            edited = input("Enter the edited response: ")
            state["human_decision"] = edited

            # ✅ SAVE MEMORY
            save_memory(email, edited)

        elif choice == "2":
            state["human_decision"] = "deny"
        else:
            state["human_decision"] = "approve"

    print("\n--- HUMAN DECISION ---")
    print("Final Action:", state["human_decision"])
    print("Time:", datetime.now())

    return state
