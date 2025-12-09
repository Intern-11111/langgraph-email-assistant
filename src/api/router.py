from fastapi import APIRouter
from src.api.models import EmailRequest, TriageResult
from src.graph.email_graph import build_graph
from src.graph.state import EmailState

router = APIRouter()
graph = build_graph()


@router.post("/email", response_model=TriageResult)
def triage_api(request: EmailRequest):
    # You can still build EmailState (LangGraph converts it internally),
    # but the compiled graph returns a dict-like state.
    state = EmailState(email_content=request.email)
    result = graph.invoke(state)

    # result is a dict: {"email_content": "...", "triage_decision": "...", ...}
    return TriageResult(
        decision=result.get("triage_decision", "notify_human"),
        confidence=result.get("triage_confidence", 0.0),
        reason=result.get("triage_reason", "no reason provided"),
    )
