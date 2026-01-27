from fastapi import APIRouter
from uuid import uuid4

from src.api.models import EmailRequest, TriageResult
from src.graph.email_graph import build_graph
from src.graph.state import EmailState
from src.state.thread_registry import THREAD_REGISTRY

# 🔹 HITL router
from src.api.hitl_router import router as hitl_router

router = APIRouter()

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

    # --------------------------------------------------
    # 1️⃣ Generate and REGISTER thread_id (CRITICAL)
    # --------------------------------------------------
    thread_id = str(uuid4())

    # 🔑 This is what makes the thread visible to /debug/hitl/threads
    THREAD_REGISTRY.add(thread_id)

    # --------------------------------------------------
    # 2️⃣ Get graph (singleton)
    # --------------------------------------------------
    graph = get_graph()

    # --------------------------------------------------
    # 3️⃣ Build initial graph state
    # --------------------------------------------------
    state = EmailState(
        email_content=request.email,
        from_email=request.from_email,
        subject=request.subject,
    )

    # --------------------------------------------------
    # 4️⃣ Invoke graph with CORRECT config shape
    # --------------------------------------------------
    result = graph.invoke(
        state,
        config={"configurable": {"thread_id": thread_id}}
    )

    # Helpful for manual testing / logs
    print("THREAD_ID:", thread_id)

    # --------------------------------------------------
    # 5️⃣ HITL pause handling
    # --------------------------------------------------
    if result.get("hitl_required"):
        print("HITL PAUSED, awaiting human decision...")
        return TriageResult(
            decision="notify_human",
            confidence=1.0,
            reason="Awaiting human approval (HITL)",
        )

    # --------------------------------------------------
    # 6️⃣ Normal completion
    # --------------------------------------------------
    return TriageResult(
        decision=result.get("triage_decision", "notify_human"),
        confidence=result.get("triage_confidence", 0.0),
        reason=result.get("triage_reason", "no reason provided"),
    )