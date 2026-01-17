import re

def enforce_name_preference(draft: str, preferred_name: str) -> str:
    """
    Force the greeting to use the preferred name.
    This runs AFTER the LLM, so it is deterministic.
    """

    if not draft or not preferred_name:
        return draft

    # Normalize whitespace
    text = draft.strip()

    # Case 1: Replace existing greeting
    text = re.sub(
        r"^(dear|hi|hello)\s+\w+[,]?",
        f"Dear {preferred_name},",
        text,
        flags=re.IGNORECASE,
    )

    # Case 2: If no greeting at all, prepend one
    if not re.match(r"^(dear|hi|hello)\s", text, re.IGNORECASE):
        text = f"Dear {preferred_name},\n\n{text}"

    return text
