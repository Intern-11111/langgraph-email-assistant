from langgraph.checkpoint.memory import MemorySaver

# Checkpointer for Milestone 3 (HITL pause & resume)
# This safely saves agent state during interrupts
checkpointer = MemorySaver()
