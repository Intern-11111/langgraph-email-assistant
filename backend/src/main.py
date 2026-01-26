"""
Production-Ready FastAPI Backend
Integrates LangGraph workflow with HTTP endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

# Import graph and HITL handler
from backend.src.graph import create_graph
from langgraph.checkpoint.memory import MemorySaver
from backend.src.hitl_handler import handle_hitl

# Initialize graph with memory
memory_saver = MemorySaver()
email_graph = create_graph(checkpointer=memory_saver)

app = FastAPI(
    title="Email Assistant - Template Based",
    description="Email Agent with Keyword Categorization and Template Responses (No LLM)",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str
    thread_id: Optional[str] = None


class HITLDecision(BaseModel):
    thread_id: str
    decision: str  # "approve", "deny", or "edit"
    edited_args: Optional[Dict] = None


@app.get("/")
def read_root():
    """API health check and info."""
    return {
        "message": "Email Assistant - Template Based (No LLM)",
        "version": "3.0.0",
        "status": "active",
        "features": [
            "Keyword-Based Email Triage",
            "Template Response Generation",
            "HITL Safety Checkpoints",
            "Mock Tools (Gmail & Calendar)",
            "No LLM - Runs Offline"
        ],
        "endpoints": {
            "process_email": "POST /v1/process-email",
            "hitl_decision": "POST /v1/hitl-decision",
            "get_status": "GET /v1/status/{thread_id}"
        }
    }


@app.post("/v1/process-email")
def process_email(request: EmailRequest):
    """
    Process an email through the LangGraph workflow.
    
    Returns either a final result or HITL checkpoint data requiring human approval.
    """
    try:
        # Generate thread ID if not provided
        thread_id = request.thread_id or f"email-{uuid.uuid4().hex[:8]}"
        
        # Create initial state (simplified for template-based workflow)
        state = {
            "mail": {
                "id": thread_id,
                "sender": request.sender,
                "subject": request.subject,
                "body": request.body
            },
            "userid": "default_user",
            "triage_category": None,
            "action_type": None,
            "action_args": None,
            "final_reply": None,
            "hitl": None,
            "hitl_decision": None
        }
        
        # Execute graph workflow
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            result = email_graph.invoke(state, config=config)
        except Exception as graph_error:
            # If graph execution fails, return error in expected format
            return {
                "status": "error",
                "thread_id": thread_id,
                "hitl_required": False,
                "message": f"Graph execution error: {str(graph_error)}",
                "error_type": type(graph_error).__name__
            }
        
        # Check if workflow paused at HITL checkpoint
        if result.get("hitl_decision") == "pending":
            return {
                "status": "pending_hitl",
                "thread_id": thread_id,
                "hitl_required": True,
                "triage_category": result.get("triage_category"),
                "proposed_action": result.get("hitl"),
                "message": "Workflow paused - awaiting human approval"
            }
        
        # Return completed workflow result
        return {
            "status": "completed",
            "thread_id": thread_id,
            "hitl_required": False,
            "triage_category": result.get("triage_category"),
            "final_reply": result.get("final_reply"),
            "message": "Email processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing email: {str(e)}"
        )


@app.post("/v1/hitl-decision")
def hitl_decision(decision: HITLDecision):
    """
    Apply human decision and resume graph execution.
    
    Decisions: "approve", "deny", or "edit"
    """
    try:
        config = {"configurable": {"thread_id": decision.thread_id}}
        
        # Apply human decision to graph state
        handle_hitl(
            app=email_graph,
            config=config,
            decision=decision.decision,
            edit_values=decision.edited_args
        )
        
        # Resume workflow execution
        result = email_graph.invoke(None, config=config)
        
        return {
            "status": "completed",
            "thread_id": decision.thread_id,
            "decision_applied": decision.decision,
            "final_reply": result.get("final_reply"),
            "tool_result": result.get("tool_result"), # Pass tool result to frontend
            "message": f"Action {decision.decision}d and executed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing decision: {str(e)}"
        )


@app.get("/v1/status/{thread_id}")
def get_status(thread_id: str):
    """
    Get current state of a workflow by thread ID.
    
    Useful for debugging and monitoring.
    """
    try:
        config = {"configurable": {"thread_id": thread_id}}
        state = email_graph.get_state(config)
        
        return {
            "thread_id": thread_id,
            "state": state.values,
            "next_steps": state.next,
            "metadata": {
                "checkpoint_id": str(state.config.get("configurable", {}).get("checkpoint_id", "N/A")),
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Thread not found: {str(e)}"
        )


@app.get("/v1/health")
def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "graph_compiled": email_graph is not None,
        "memory_enabled": memory_saver is not None
    }


if __name__ == "__main__":
    print("\nStarting Email Assistant API Server...")