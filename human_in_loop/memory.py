memory_store = {}

def save_memory(email, decision):
    memory_store[email] = decision

def load_memory(email):
    return memory_store.get(email)
