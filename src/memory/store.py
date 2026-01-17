import sqlite3
from typing import Dict

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            namespace TEXT,
            key TEXT,
            value TEXT,
            PRIMARY KEY (namespace, key)
        )
    """)
    conn.commit()
    conn.close()


def save_memory(namespace: str, key: str, value: str):
    """
    Save or update a memory value.
    namespace = thread_id / user_id / global
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO memory (namespace, key, value)
        VALUES (?, ?, ?)
        ON CONFLICT(namespace, key)
        DO UPDATE SET value = excluded.value
        """,
        (namespace, key, value),
    )
    conn.commit()
    conn.close()


def load_memory(namespace: str) -> Dict[str, str]:
    """
    Load all memory for a namespace.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT key, value FROM memory WHERE namespace = ?",
        (namespace,),
    ).fetchall()
    conn.close()

    return {k: v for k, v in rows}

# def load_all_memory() -> Dict[str, Dict[str, str]]:
#     """
#     Load all memory across all namespaces.
#     """
#     init_db()
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     rows = cur.execute(
#         "SELECT namespace, key, value FROM memory"
#     ).fetchall()
#     conn.close()

#     memory = {}
#     for namespace, key, value in rows:
#         if namespace not in memory:
#             memory[namespace] = {}
#         memory[namespace][key] = value

#     return memory