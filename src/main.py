from src.agents.hello_agent import hello_agent_demo

def run():
    print("Running Hello Agent demo...")
    reply = hello_agent_demo("Hello! Can you introduce yourself briefly for our team project?")
    print("\n----- LLM Response -----\n")
    print(reply)

if __name__ == "__main__":
    run()
