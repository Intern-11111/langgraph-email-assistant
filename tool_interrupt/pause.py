def pause_before_tool(state):
    print("\n⚠️ INTERRUPT TRIGGERED ⚠️")
    print("Sensitive action detected: send_email")
    print("Waiting for human approval...")

    print("\nChoose one option:")
    print("1. approve")
    print("2. deny")

    choice = input("Your choice: ").strip()

    if choice == "1":
        state["approved"] = True
    else:
        state["approved"] = False

    return state
