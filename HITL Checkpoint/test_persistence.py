import time
from graph import app

def demonstrate_milestone():
    #Using a unique thread ID
    config = {"configurable": {"thread_id": "milestone_demo_123"}}
    
    print("---Stage 1: INITIAL PROCESSING ---")
    initial_input = {
        "mail": {"subject": "Urgent", "body": "Send the report now."},
        "messages": [("user", "Draft and send this email.")]
    }
    
    # Run the agent until it hits the HITL interrupt
    for event in app.stream(initial_input, config):
        print(f"Current Node: {list(event.keys())[0]}")

    print("\nSYSTEM PAUSED: HITL Interrupt triggered.")
    print("Verification: Check your folder for 'checkpoints.sqlite'.")
    print("The agent is now 'asleep' in the database.")
    
    # Simulating a "crash" or waiting period
    for i in range(3, 0, -1):
        print(f"Simulating system wait... {i}")
        time.sleep(1)

    print("\n--- STAGE 2: RECOVERING FROM DATABASE ---")
    #passing 'None' because the state is recovered from SQLite
    print("Resuming based on thread_id...")
    for event in app.stream(None, config):
        print(f"Resumed Node: {list(event.keys())[0]}")
    
if __name__ == "__main__":
    demonstrate_milestone()
