from fastapi import APIRouter
from uuid import uuid4

from src.api.models import EmailRequest, TriageResult
from src.graph.email_graph import build_graph
from src.graph.state import EmailState

# 🔹 HITL router
from src.api.hitl_router import router as hitl_router

router = APIRouter()

# ============================================================
# Build LangGraph ONCE (critical for HITL + multiprocessing)
# ============================================================


# Register HITL routes
router.include_router(hitl_router)


from fastapi import APIRouter
from uuid import uuid4

from src.api.models import EmailRequest, TriageResult
from src.graph.state import EmailState
from src.graph.graph_registry import get_graph

# HITL router
from src.api.hitl_router import router as hitl_router

router = APIRouter()
router.include_router(hitl_router)


@router.post("/email", response_model=TriageResult)
def triage_api(request: EmailRequest):
    """
    Entry point for processing a new email.
    May PAUSE if a dangerous action is planned.
    """

    # Unique thread_id is REQUIRED for HITL resume
    thread_id = str(uuid4())

    # ✅ ALWAYS get graph from registry
    graph = get_graph()

    state = EmailState(email_content=request.email)

    result = graph.invoke(
        state,
        config={"thread_id": thread_id}
    )

    # Helpful for manual testing
    print("THREAD_ID:", thread_id)

    #  HITL: graph paused before action_node
    if result.get("hitl_required"):
        print("HITL PAUSED, awaiting human decision...")
        return TriageResult(
            decision="notify_human",
            confidence=1.0,
            reason="Awaiting human approval (HITL)",
        )

    return TriageResult(
        decision=result.get("triage_decision", "notify_human"),
        confidence=result.get("triage_confidence", 0.0),
        reason=result.get("triage_reason", "no reason provided"),
    )
