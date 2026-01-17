from src.memory.store import save_memory

def learn_from_edit(original: str, edited: str):
    if "bob" in original.lower() and "robert" in edited.lower():
        save_memory("preferred_name", "Robert")
