def log(state, message: str):
    """
    Persist execution logs inside LangGraph state
    and also print to terminal.
    """
    print(message)

    if not hasattr(state, "execution_logs") or state.execution_logs is None:
        state.execution_logs = []

    state.execution_logs.append(message)
