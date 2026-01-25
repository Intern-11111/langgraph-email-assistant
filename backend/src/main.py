# Backend API - Simplified for Milestone 4 (HITL + Memory)
# Using only read_calendar and send_mail tools

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

# Import simplified tools
from backend.src.tools.tools import read_calendar, send_mail, AVAILABLE_TOOLS

app = FastAPI(
    title="Email Assistant - HITL Backend",
    description="Milestone 4: HITL Workflow with Persistent Memory",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class EmailRequest(BaseModel):
    subject: str
    body: str
    thread_id: str = "email-thread"

class HITLDecision(BaseModel):
    thread_id: str
    decision: str  # "approve", "edit", "deny"
    edited_args: Optional[Dict] = None

# In-memory state storage (Milestone 4: Memory)
SESSIONS = {}

@app.get("/")
def read_root():
    return {
        "message": "Email Assistant - HITL Backend",
        "mode": "Milestone 4",
        "tools": ["read_calendar", "send_mail"],
        "team": ["Payal (HITL/Memory)", "Samruddhi (Tools)", "Ganesh (Triage)"]
    }

@app.post("/v1/process-email")
async def process_email(request: EmailRequest):
    """
    Process email through triage and agent workflow.
    Returns HITL checkpoint if dangerous action detected.
    """
    try:
        thread_id = request.thread_id
        
        # Simple triage logic (Ganesh M1)
        body_lower = request.body.lower()
        
        # Ignore spam/newsletters
        if any(word in body_lower for word in ["unsubscribe", "newsletter", "promotion"]):
            return {
                "status": "ignored",
                "hitl_required": False,
                "message": "Email ignored (spam/newsletter)"
            }
        
        # Check if meeting-related (needs calendar tool)
        if any(word in body_lower for word in ["meet", "schedule", "calendar", "appointment"]):
            # Read calendar first
            events = read_calendar()
            
            # Format events as human-readable text
            events_text = "\n".join([
                f"• {event['title']} at {event['time']}"
                for event in events[:2]
            ])
            
            # Propose sending meeting confirmation
            proposed_action = {
                "tool": "send_mail",
                "args": {
                    "to": "sender@example.com",  # In real system, extract from email
                    "subject": f"Re: {request.subject}",
                    "body": f"Thanks for your email about '{request.subject}'.\n\n"
                            f"I have the following on my calendar:\n{events_text}\n\n"
                            f"Let me know what works best for you."
                }
            }
            
            # HITL Checkpoint (Payal M3)
            SESSIONS[thread_id] = {
                "email": {"subject": request.subject, "body": request.body},
                "proposed_action": proposed_action,
                "calendar_events": events
            }
            
            return {
                "status": "pending_approval",
                "hitl_required": True,
                "proposed_action": proposed_action,
                "calendar_events": events
            }
        
        # Simple acknowledgment
        else:
            # Auto-approve for simple replies
            return {
                "status": "completed",
                "hitl_required": False,
                "final_reply": f"Thank you for your email regarding '{request.subject}'. I've received it and will respond shortly.",
                "tool_result": None
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")

@app.post("/v1/hitl-decision")
async def hitl_decision(decision: HITLDecision):
    """
    Handle HITL decision (approve/edit/deny).
    Payal M3: HITL workflow
    """
    try:
        thread_id = decision.thread_id
        
        if thread_id not in SESSIONS:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = SESSIONS[thread_id]
        proposed_action = session["proposed_action"]
        
        # User Approved
        if decision.decision == "approve":
            tool_name = proposed_action["tool"]
            tool_args = proposed_action["args"]
            
            # Execute tool
            if tool_name in AVAILABLE_TOOLS:
                result = AVAILABLE_TOOLS[tool_name](**tool_args)
                
                # Cleanup session (Milestone 4: Memory management)
                del SESSIONS[thread_id]
                
                return {
                    "status": "completed",
                    "hitl_required": False,
                    "tool_result": result,
                    "message": f"{tool_name} executed successfully"
                }
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        # User Edited
        elif decision.decision == "edit":
            tool_name = proposed_action["tool"]
            tool_args = proposed_action["args"].copy()
            
            # Apply edits
            if decision.edited_args:
                tool_args.update(decision.edited_args)
            
            # Execute with edited args
            if tool_name in AVAILABLE_TOOLS:
                result = AVAILABLE_TOOLS[tool_name](**tool_args)
                
                # Cleanup session
                del SESSIONS[thread_id]
                
                return {
                    "status": "completed",
                    "hitl_required": False,
                    "tool_result": result,
                    "message": f"{tool_name} executed with edits"
                }
        
        # User Denied
        elif decision.decision == "deny":
            # Cleanup session
            del SESSIONS[thread_id]
            
            return {
                "status": "denied",
                "hitl_required": False,
                "message": "Action denied by user"
            }
        
        else:
            raise HTTPException(status_code=400, detail="Invalid decision")
            
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Session error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing decision: {str(e)}")

@app.get("/v1/tools")
def get_available_tools():
    """List available tools"""
    return {
        "tools": list(AVAILABLE_TOOLS.keys()),
        "descriptions": {
            "read_calendar": "View scheduled calendar events (Samruddhi M1)",
            "send_mail": "Send email response (Payal M4 HITL)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)