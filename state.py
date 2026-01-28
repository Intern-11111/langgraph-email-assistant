from typing import TypedDict,List , Optional

class EmailState(TypedDict):
    sender: str
    subject: str
    body: str

    category: Optional[str]      # ignore | notify_human | respond
    intent: Optional[str]

    requires_approval: bool
    approved: Optional[bool]
    action_taken: Optional[str]
