"""
Node functions for the email agent workflow.
Hybrid Architecture: LLM for Triage + Templates for Responses.
"""
from typing import Literal, Dict, Any, Annotated
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langgraph.types import RunnableConfig

from backend.src.state import AgentState
from backend.src.config import gemini_ai_model
from backend.src.templates import get_template_for_email
from backend.src.tools.mock_gmail import mark_as_processed, send_reply
from backend.src.tools.mock_calendar import create_calendar_event

# Initialize LLM only for triage
try:
    llm = gemini_ai_model()
except Exception as e:
    print(f"LLM not available: {e}. Falling back to keyword triage.")
    llm = None


# Define dangerous actions that require human approval
DANGEROUS_ACTIONS = ["send_reply", "create_calendar_event"]


# --- LLM Triage Definition ---
class Category(BaseModel):
    category: Annotated[Literal["ignore","notify-human","respond-act"], "The classification of the email based on the rules."]

parser = PydanticOutputParser(pydantic_object=Category)

triage_prompt = PromptTemplate(template="""
    ("system", "You are an email categorization assistant. CRITICAL RULES (follow exactly)
            1. ignore =Spam, newsletters, ads, unsubscribe, promotions
            2. respond-act = ANY meeting request, scheduling, simple questions, 
                info requests, replies agent can draft (maximum cases!)
            3. notify-human = ONLY: URGENT emergencies, complaints, legal/HR, 
                confidential, unclear high-risk
            PRIORITIZE respond-act for ALL meetings/scheduling!"),
                        
    ("human",
    Analyze the following email and categorize it.
                        Subject:{subject}
                        Body:{body}
    
   
    
    IMPORTANT RULES:
    1. Return ONLY the JSON object. 
    2. Do NOT add any preamble like "Here is the JSON".
    3. Do NOT add any explanation after the JSON.
    4. Do NOT use Markdown formatting (no ```json blocks). Just raw JSON.
""",
input_variables=["subject", "body"],
partial_variables={"format_instructions": parser.get_format_instructions()}
)


def categorize_email_llm(subject: str, body: str) -> str:
    """
    Categorize email using Gemini LLM.
    Falls back to keywords if LLM fails.
    """
    if not llm:
        return categorize_email_keywords(subject, body)
        
    try:
        chain = triage_prompt | llm | parser
        result = chain.invoke({"subject": subject, "body": body})
        return result.category
    except Exception as e:
        print(f"LLM Triage Failed: {e}. Falling back to keywords.")
        return categorize_email_keywords(subject, body)


def categorize_email_keywords(subject: str, body: str) -> str:
    """
    Backup keyword-based categorization.
    """
    subject_lower = subject.lower()
    body_lower = body.lower()
    combined = subject_lower + " " + body_lower
    
    ignore_keywords = ['unsubscribe', 'newsletter', 'promotion', 'marketing', 'sale', 'offer']
    if any(k in combined for k in ignore_keywords): return "ignore"
    
    notify_keywords = ['urgent', 'emergency', 'complaint', 'legal', 'confidential']
    if any(k in combined for k in notify_keywords): return "notify-human"
    
    return "respond-act"


def triage_node(state: AgentState) -> AgentState:
    """
    Categorize the incoming email using hybrid approach (LLM preferred).
    """
    mail = state['mail']
    
    # Use LLM for categorization
    category = categorize_email_llm(mail['subject'], mail['body'])
    
    print(f"Triage Result: {category}")
    
    return {"triage_category": category}


def check_route(state: AgentState) -> Literal["ignore", "notify-human", "respond-act"]:
    """
    Route to the appropriate handler based on triage category.
    """
    category = state.get("triage_category", "notify-human")
    if category in ["ignore", "notify-human", "respond-act"]:
        return category
    return "notify-human"


def generate_response_node(state: AgentState) -> AgentState:
    """
    Generate email response using TEMPLATES (no LLM here).
    """
    mail = state['mail']
    category = state.get('triage_category', 'respond-act')
    
    # Get template-based response
    reply = get_template_for_email(mail, category)
    
    if reply:
        print(f"Generated template response ({len(reply)} chars)")
        return {
            "final_reply": reply,
            "action_type": "send_reply",
            "action_args": {
                "to": mail['sender'],
                "subject": f"Re: {mail['subject']}",
                "body": reply
            },
            "hitl": {
                "action": "send_reply",
                "args": {
                    "to": mail['sender'],
                    "subject": f"Re: {mail['subject']}",
                    "body": reply
                },
                "proposed_reply": reply,
                "triage": category
            },
            "hitl_decision": "pending"
        }
    else:
        print("No response needed for this email")
        return {
            "final_reply": None,
            "action_type": None,
            "action_args": None,
            "hitl": None,
            "hitl_decision": None
        }


def hitl_checkpoint(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Execute approved action after human review.
    """
    decision = state.get("hitl_decision")
    action_type = state.get("action_type")
    action_args = state.get("action_args") or {}
    mail = state.get("mail")
    
    if not action_type or not decision or decision == "pending":
        return state
    
    if decision == "deny":
        print("HITL: Action denied by human.")
        return {
            "final_reply": "Action cancelled by human.",
            "tool_result": "Action denied by user.",
            "hitl_decision": "processed",
            "action_type": None
        }
    
    if decision in ("approve", "edit"):
        result = None
        
        if action_type == "send_reply":
            reply_content = state.get("final_reply")
            result = send_reply(
                to=mail["sender"],
                subject=f"Re: {mail['subject']}",
                body=reply_content
            )
            print(f"Email reply sent (mock): {result}")
        
        elif action_type == "create_calendar_event":
            result = create_calendar_event(
                summary=action_args.get("summary", "Meeting"),
                start=action_args.get("start", "2026-01-28T14:00:00"),
                end=action_args.get("end", "2026-01-28T15:00:00")
            )
            print(f"Calendar event created (mock): {result}")
        
        if result and mail:
            mark_as_processed(mail["id"])
        
        confirm_text = f"Executed {action_type}. Result: {result}"
        final_output = state.get("final_reply") if action_type == "send_reply" else confirm_text
        
        return {
            "final_reply": final_output,
            "tool_result": confirm_text,
            "hitl_decision": "processed",
            "action_type": None
        }
    
    return state


def ignore(state: AgentState, config: RunnableConfig) -> AgentState:
    print("Ignored email (spam or promotion).")
    if state.get("mail"): mark_as_processed(state["mail"]["id"])
    return state


def notify_human(state: AgentState, config: RunnableConfig) -> AgentState:
    print("Notifying human: email needs attention.")
    if state.get("mail"): mark_as_processed(state["mail"]["id"])
    return state
