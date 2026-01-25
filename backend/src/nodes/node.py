from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from pydantic import Field,BaseModel
from backend.src.state import AgentState
from backend.src.config import gemini_ai_model
from backend.src.tools.tools import send_gmail_reply, read_calendar_availability, get_user_prefs, DANGEROUS_TOOLS
# UPDATED: Use mock tools instead of real APIs
from backend.src.tools.mock_gmail import mark_as_processed, send_reply
from backend.src.tools.mock_calendar import create_calendar_event, check_availability
from typing import Literal,Annotated,Dict,Any,List
from langchain_core.output_parsers import PydanticOutputParser
from datetime import timedelta, timezone, datetime
import dateparser

# Mock timezone (since we removed google_calendar IST)
from datetime import timezone
IST = timezone(timedelta(hours=5, minutes=30))

from langgraph.graph.message import add_messages
import re
import json

import time
from google.api_core import exceptions
model_gemini=gemini_ai_model()



class Category(BaseModel):
    category: Annotated[Literal["ignore","notify-human","respond-act"],"The classification of the email based on the rules."]

parser=PydanticOutputParser(pydantic_object=Category)

prompt = PromptTemplate(template="""
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

react_prompt = """
You are an email assistant. MANDATORY RULES:
1. Meeting/schedule → read_calendar_availability(start='YYYY-MM-DD HH:MM', end='...')
2. Before reply → get_user_prefs()
3. Reply → send_gmail_reply(to=..., subject=..., body=...)

JSON tools only:
- "tool": "read_calendar_availability", "args": {"start": "...", "end": "..."}
- "tool": "get_user_prefs", "args": {}
- "tool": "send_gmail_reply", "args": {"to": "bob@...", "subject": "...", "body": "..."}

Final answer: natural language only.
"""
# node function
async def triage_node(state:AgentState)->AgentState:
    mail=state['mail']

    chain=prompt|model_gemini|parser
    result_obj=await chain.ainvoke({"subject":mail['subject'],"body":mail['body']})
    #Extract the actual string from the object
    category_str=result_obj.category

    print(f"✅ Triage: {category_str}")

    return {"triage_category":category_str}


def check_route(state: AgentState)->Literal["ignore","notify-human","respond-act"]:

    if state["triage_category"]=="ignore":
        return "ignore"
    elif state["triage_category"]=="notify-human":
        return "notify-human"
    elif state["triage_category"]=="respond-act":
        return "respond-act"
    else:
        return "notify-human"        #safe 
    
# def react_route(state: AgentState) -> str:
#     """Route the ReAct loop. Stop immediately when we have a final reply."""
    
#     # DEBUG: Log state values to trace the issue
#     print(f"🔀 ROUTER: final_reply={bool(state.get('final_reply'))}, tool_name={state.get('tool_name')}, hitl_decision={state.get('hitl_decision')}")
    
#     # 1. If HITL decision was processed and we have a tool to execute
#     if state.get("hitl_decision") == "processed" and state.get("tool_name"):
#         print("🔀 ROUTER → react_tools (HITL processed)")
#         return "react_tools"
    
#     # 2. If we have a pending HITL envelope → go to checkpoint
#     if state.get("hitl") and state.get("hitl_decision") == "pending":
#         print("🔀 ROUTER → hitl_checkpoint")
#         return "hitl_checkpoint"

#     # 3. If we have a final reply and no pending tool → STOP (most important check)
#     if state.get("final_reply") and not state.get("tool_name"):
#         print("🔀 ROUTER → react_end (FINAL REPLY EXISTS!)")
#         return "react_end"

#     # 4. If we have a tool to execute
#     if state.get("tool_name"):
#         # If tool is dangerous, route to HITL
#         if state["tool_name"] in DANGEROUS_TOOLS:
#             print(f"🔀 ROUTER → hitl_checkpoint (dangerous tool: {state['tool_name']})")
#             return "hitl_checkpoint"
#         # Otherwise execute the safe tool
#         print(f"🔀 ROUTER → react_tools (safe tool: {state['tool_name']})")
#         return "react_tools"

#     # 5. If triage says respond-act but no final reply yet → continue loop
#     if state.get("triage_category") == "respond-act" and not state.get("final_reply"):
#         print("🔀 ROUTER → react_model (no final_reply yet)")
#         return "react_model"

#     if not state.get("tool_name") and not state.get("final_reply"):
#     # If the LLM didn't give a tool AND didn't give a reply, 
#     # it's confused. Force it to generate a draft or end.
#         return "react_model"

#     # 6. Default: end the workflow
#     print("🔀 ROUTER → react_end (default)")
#     return "react_end"

def react_route(state: AgentState) -> str:
    # 1. STOP immediately if we have a final reply
    if state.get("final_reply"):
        print("🔀 ROUTER → react_end (FINAL REPLY EXISTS!)")
        return "react_end"

    # 2. Check for Tool Calls
    tool_name = state.get("tool_name")
    if tool_name:
        if tool_name in DANGEROUS_TOOLS:
            print(f"🔀 ROUTER → hitl_checkpoint (dangerous tool: {tool_name})")
            return "hitl_checkpoint"
        print(f"🔀 ROUTER → react_tools (safe tool: {tool_name})")
        return "react_tools"

    # 3. Handle HITL Decisions
    if state.get("hitl_decision") == "pending":
        return "hitl_checkpoint"

    # 4. SAFETY: Handle the Empty LLM Response (The loop you saw)
    # If there is no tool_name and no final_reply, the LLM failed to act.
    messages = state.get("messages", [])
    if messages and messages[-1].content.strip() == "":
        print("⚠️ ROUTER: LLM returned empty string. Forcing termination to prevent loop.")
        # Instead of going back to react_model, we force it to end 
        # or you can route to a "recovery" node that writes a generic apology.
        return "react_end"

    # 5. Continue if work is still needed
    if state.get("triage_category") == "respond-act":
        print("🔀 ROUTER → react_model (logic check)")
        return "react_model"

    return "react_end"

# def react_model_node(state: AgentState) -> AgentState:
#     mail = state["mail"]
#     # 1. Get messages from state
#     messages = state.get("messages", []).copy()

#     next_tue_str = (datetime.now() + timedelta(days=(1 - datetime.now().weekday() + 7) % 7)).strftime("%Y-%m-%d")
    
#     # 2. Add System and Human message only once
#     if len(messages) == 0:
#         today_str = datetime.now().strftime("%Y-%m-%d")
#         react_prompt = f"""
#         You are a production email assistant. FULLY autonomous workflow:

#         📋 TODAY: {datetime.now().strftime('%Y-%m-%d %H:%M IST')}

#         MANDATORY WORKFLOW (ALWAYS complete sequence):
#         1. **MEETINGS**: extract_meeting_from_email() → read_calendar_availability() → create_calendar() → send_gmail_reply()
#         2. **REPLIES**: get_user_prefs() → send_gmail_reply()
#         3. **PROCESS**: process_email() after handling

#         🛡️ DANGEROUS TOOLS (agent PAUSES for HITL):
#         • create_calendar() → Books REAL meeting
#         • send_gmail_reply() → Sends REAL email

#         📖 SAFE TOOLS (auto-execute):
#         • read_calendar_availability() → Check slots
#         • extract_meeting_from_email() → Parse dates
#         • get_user_prefs() → Signature/style
#         • process_email() → Mark done

#         🎯 TOOL USAGE RULES:
#         "meeting/schedule/confirm/book/time" → extract_meeting → read_calendar → create_calendar → reply
#         "reply/send/confirm" → get_user_prefs → send_gmail_reply  
#         "done/processed" → process_email()
#         ALWAYS get_user_prefs before send_gmail_reply!

#         📨 JSON FORMAT (exact):
#         {{"tool": "read_calendar_availability", "args": {{"start": "2026-01-03T14:00:00", "end": "2026-01-03T15:00:00"}}}}

#         📅 DATE FORMAT: YYYY-MM-DDTHH:MM:SS (IST timezone)

#         EXAMPLES:
#         Email: "Meet Tue 2PM?" → extract_meeting → read_calendar → create_calendar → reply
#         Email: "Thanks!" → get_user_prefs → send_gmail_reply  
#         Email: "Confirm?" → read_calendar → reply + process_email

#         FINAL natural language ONLY when ALL tools complete.
#         """

#         user_content = f"EMAIL:\nSubject: {mail['subject']}\nBody: {mail['body']}"
#         messages.append(SystemMessage(content=react_prompt))
#         messages.append(HumanMessage(content=user_content))
    
#     # 3. Invoke model
#     resp = model_gemini.invoke(messages)
#     content = resp.content

#     # Handle Gemini format
#     if isinstance(content, list):
#         text = " ".join([getattr(b, 'text', b.get('text', '')) for b in content]).strip()
#     else:
#         text = str(content).strip()

#     # Generic multi-JSON parser
#     def extract_tool_calls(text: str):
#         tool_calls = []
#         json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
#         for i, match in enumerate(json_matches):
#             try:
#                 obj = json.loads(match)
#                 if "tool" in obj:
#                     tool_calls.append({
#                         "name": obj["tool"],
#                         "args": obj.get("args", {}),
#                         "id": f"call_{obj['tool']}_{i}"
#                     })
#             except json.JSONDecodeError:
#                 continue
#         return tool_calls

#     tool_calls = extract_tool_calls(text)
#     print(f"🔧 Found {len(tool_calls)} tools: {[tc['name'] for tc in tool_calls]}")

#     if tool_calls:
#         first_tool = tool_calls[0]
#         # IMPORTANT: Append the model's actual response (resp) to history 
#         # so it knows it initiated a tool call.
#         messages.append(resp) 
        
#         print(f"🔧 ReAct: {first_tool['name']} → {first_tool['args']}")
#         return {
#             "messages": messages,
#             "tool_name": first_tool["name"],
#             "tool_args": first_tool["args"],
#             "final_reply": None
#         }
#     else:
#         print("💬 ReAct: Final reply")
#         # Append the final answer to history
#         messages.append(resp)
#         return {
#             "messages": messages,
#             "final_reply": text,
#             "tool_name": None,
#             "tool_args": None
#         }

async def react_model_node(state: AgentState) -> AgentState:
    """Generate LLM response for ReAct loop. Skips if final reply already exists."""
    
    # Early termination: if we already have a final reply, don't re-run the model
    if state.get("final_reply") and not state.get("tool_name"):
        print("⏭️ Skipping model - final reply already exists")
        return state
    
    mail = state["mail"]
    messages: List[Any] = state.get("messages", []).copy()

    # --- 🛡️ LOOP SAFEGUARD 🛡️ ---
    # If the conversation gets too long (e.g., > 15 turns), force termination to prevent money burning loops
    if len(messages) > 15:
        print("⚠️ LOOP DETECTED: Forcefully terminating agent after 15 turns.")
        return {
            "messages": messages,
            "final_reply": "I apologize, but I'm having trouble processing this request automatically. Please handle this email manually.",
            "tool_name": None,
            "tool_args": {},
            "hitl": None,
            "hitl_decision": None
        }

    # 1) Build dynamic date context
    now_ist = datetime.now(IST)
    
    # MOCK: Simple event extraction
    def extract_event_details_mock(body: str, subject: str) -> Dict:
        """Mock event extraction - looks for basic meeting keywords"""
        body_lower = body.lower()
        if "meet" in body_lower or "schedule" in body_lower or "calendar" in body_lower:
            return {
                "summary": subject,
                "slots": [{"start": "2026-01-28T14:00:00", "end": "2026-01-28T15:00:00"}]
            }
        return None
    
    event_details = extract_event_details_mock(mail["body"], mail["subject"])

    date_context = f"""
    📅 LIVE DATE PARSING (IST):
    Today: {now_ist.strftime('%Y-%m-%d %A %H:%M')}
    LLM Extracted: {json.dumps(event_details) if event_details else 'None'}

    Slots parsed: {event_details.get('slots', []) if event_details else []}
    """

    # 2) System prompt
    react_prompt = f"""Production Email Assistant - FULL AUTONOMY
    
    {date_context}
    
    📋 YOUR TASK: Process emails autonomously using tools, then draft replies.
    
    🔄 MANDATORY WORKFLOW (Follow these paths EXACTLY):
    
    Path A: MEETING REQUEST (e.g. "Can we meet?", "Schedule a call")
      1. `extract_meeting_from_email` (You usually have this from context)
      2. `read_calendar_availability` (Check if the requested slot is free)
         - If FREE: `create_calendar` (BOOK IT IMMEDIATELY. Do NOT ask user "Should I book?". Just book it.)
         - If BUSY: `create_calendar` (Book the next best alternative if implied, or propose new time in reply)
      3. `send_gmail_reply` (Confirming the meeting is booked)
      4. DONE (Output natural language "Meeting booked and reply sent.")
    
    Path B: GENERAL REPLY / ENQUIRY (Questions, Info, Chat, Action Items)
      - Appies to: Questions, "How are you?", "Send me the report", "Thanks", etc.
      1. `get_user_prefs` (Optional, if you need signature/tone info)
      2. `send_gmail_reply` (Draft the response based on the email body)
      3. DONE
    
    Path C: PROCESSED/DONE (No Reply Needed)
      - Applies to: FYIs, newsletters, simple receipts where no acknowledgement is needed.
      - Output a final text summary like "Email processed (no reply needed)."
    
    🛑 STOPPING RULES:
    - You MUST continue calling tools until you have successfully called `send_gmail_reply` (for replies) or decided no reply is needed.
    - If you call `create_calendar`, you MUST subsequently call `send_gmail_reply` to notify the sender.
    - DO NOT end the turn with just text if there is a pending action.
    
    🛡️ DANGEROUS TOOLS (require human approval):
    - create_calendar(...)
    - send_gmail_reply(...)
    
    ✅ SAFE TOOLS:
    - extract_meeting_from_email(...)
    - read_calendar_availability(...)
    - get_user_prefs()
    
    📝 TOOL CALL FORMAT (JSON only):
    {{"tool": "read_calendar_availability", "args": {{"start": "2026-01-03T14:00:00", "end": "2026-01-03T15:00:00"}}}}
    
    IMPORTANT: 
    - If `read_calendar_availability` says "Free: True", your NEXT output MUST be `create_calendar`.
    - Do NOT stop to chat. EXECUTE.Once you have gathered all necessary information from tools, provide your final 
        response by updating the 'final_reply' field
    """

    # 3) Initialize messages for first turn
    # Note: Gemini doesn't handle SystemMessage well in conversation history
    # So we embed the system prompt in the first HumanMessage
    if not messages:
        messages.append(
            HumanMessage(content=f"{react_prompt}\n\nEMAIL TO PROCESS:\nSubject: {mail['subject']}\nBody: {mail['body']}")
        )

    # 4) Call LLM with retry
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            resp = await model_gemini.ainvoke(messages)
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"⚠️ Quota exceeded. Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise e
    else:
        # Exhausted retries
        state["final_reply"] = "I'm currently experiencing high traffic. Please try again in a minute."
        state["messages"] = messages + [AIMessage(content="Error: API Quota Exceeded after retries.")]
        state["tool_name"] = None
        state["tool_args"] = {}
        return state

    # 5) Extract tool calls from LLM text
    def extract_tool_calls(text: str) -> List[Dict[str, Any]]:
        tool_calls = []
        json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', str(text))
        for i, match in enumerate(json_matches):
            try:
                obj = json.loads(match.strip())
                if "tool" in obj:
                    tool_calls.append({
                        "name": obj["tool"],
                        "args": obj.get("args", {}),
                        "id": f"call_{obj['tool']}_{i}",
                    })
            except Exception:
                continue
        return tool_calls

    text = resp.content
    print(f"🤖 RAW LLM OUTPUT: {repr(text)}")
    tool_calls = extract_tool_calls(text)
    print(f"🔧 Found {len(tool_calls)} tools: {[tc['name'] for tc in tool_calls]}")

    # 6) If LLM emitted a tool call, set tool_name/tool_args
    if tool_calls:
        first = tool_calls[0]
        tool_name = first["name"]
        tool_args = first["args"]

        tool_msg = AIMessage(
            content="",
            tool_calls=[{
                "name": tool_name,
                "args": tool_args,
                "id": first["id"],
            }],
        )
        messages.append(tool_msg)

        state["messages"] = messages
        state["tool_name"] = tool_name
        state["tool_args"] = tool_args
        # No natural language final reply yet
        state["final_reply"] = None

        triage = state.get("triage_category")
        proposed_reply = None  # you can store something if you like

        # 7) HITL envelope for dangerous tools
        if tool_name in DANGEROUS_TOOLS:
            state["hitl"] = {
                "tool": tool_name,
                "args": tool_args,
                "proposed_reply": proposed_reply,
                "triage": triage,
            }
            state["hitl_decision"] = "pending"
        else:
            state["hitl"] = None
            state["hitl_decision"] = None

        return state 
        
    messages.append(AIMessage(content=text))
    return {
        "messages": messages,
        "final_reply": text,
        "tool_name": None,
        "tool_args": {},
        "hitl": None,
        "hitl_decision": None
    }

from langgraph.types import RunnableConfig

async def react_tools_node(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_args = state.get("tool_args") or {}
    messages = state.get("messages", []).copy()
    tool_name = state.get("tool_name")

    # Get db from config instead of state (to avoid serialization issues)
    db = config.get("configurable", {}).get("db")
    user_id = state.get("userid")


    result = None

    if tool_name == "read_calendar_availability":
        # UPDATED: Use mock calendar function
        from backend.src.tools.mock_calendar import check_availability
        
        try:
            # Mock calendar doesn't need db/user_id
            date = tool_args.get('date', 'today')
            time = tool_args.get('time', '14:00')
            result_data = check_availability(date, time)
            result = f"Available: {result_data['available']}, Conflicts: {result_data.get('conflicts', [])}"
        except Exception as e:
            result = f"Error checking calendar: {str(e)}"
    elif tool_name == "get_user_prefs":
        result = await get_user_prefs.ainvoke(tool_args)
    elif tool_name == "extract_meeting_from_email":
        if not tool_args.get("subject"):
            tool_args["subject"] = state["mail"].get("subject", "No Subject")
        if not tool_args.get("body"):
            tool_args["body"] = state["mail"].get("body", "")
        result = await extract_meeting_from_email.ainvoke(tool_args)
    elif tool_name == "process_email":
        # Handle process_email manually to inject db and user_id
        from backend.src.tools.tools import process_email
        result = await process_email.ainvoke({**tool_args, "db": db, "user_id": user_id})
    elif tool_name is None:
        result = "No tool to execute."
        
    else:
        # Dangerous or unknown tools should NOT be executed here
        result = f"Skipped execution of dangerous or unknown tool: {tool_name}"

    # Append tool result as an AIMessage for Gemini compatibility
    messages.append(AIMessage(content=f"Tool '{tool_name}' returned: {result}"))
    print(f"✅ Tool '{tool_name}' → {result}")

    # Clear tool_name/tool_args so react_route can decide next step
    # Preserve final_reply if it exists to prevent loop
    return {
        "messages": messages,
        "tool_name": None,
        "tool_args": None,
        "final_reply": state.get("final_reply") # Explicitly preserve final_reply
    }

async def hitl_checkpoint(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Handles the 'Resume' signal. Maps 'approve/edit' decisions to 
    actual tool execution for Gmail and Calendar.
    """
    decision = state.get("hitl_decision")
    hitl = state.get("hitl") or {}
    tool_name = hitl.get("tool")
    tool_args = hitl.get("args") or {}

    # Context needed for tools - get db from config
    db = config.get("configurable", {}).get("db")
    user_id = state.get("userid")
    mail = state.get("mail")

    if not tool_name or not decision or decision == "pending":
        return state

    # Path 1: User Denies
    if decision == "deny":
        print("🚫 HITL: Action Denied.")
        return {
            "final_reply": "Action cancelled by human.",
            "hitl_decision": "processed",
            "tool_name": None
        }

    # Path 2: User Approves or Edits
    if decision in ("approve", "edit"):
        result = None
        
        # Handle Gmail Sending (MOCK)
        if tool_name == "send_gmail_reply":
            # Pull the final text (updated by FastAPI if edited)
            reply_content = state.get("final_reply")
            
            # UPDATED: Use mock send_reply (no db/user_id needed)
            result = send_reply(
                to=mail["sender"],
                subject=f"Re: {mail['subject']}",
                body=reply_content
            )

        # Handle Calendar Booking (MOCK)
        elif tool_name == "create_calendar":
            # UPDATED: Use mock calendar (no service/auth needed)
            result = create_calendar_event(
                summary=tool_args.get("summary", "Meeting"),
                start=tool_args.get("start", "2026-01-28T14:00:00"),
                end=tool_args.get("end", "2026-01-28T15:00:00")
            )

        # Cleanup: Mark email as processed (MOCK)
        if result:
            mark_as_processed(mail["id"])
            print(f"✅ Workflow Complete: {tool_name} successful.")

        confirm_text = f"Executed {tool_name}. Result: {result}"
        return {
            "messages": state.get("messages", []) + [HumanMessage(content=confirm_text)],
            "final_reply": confirm_text,
            "hitl_decision": "processed",
            "tool_name": None # Clear tool so react_route can end
        }

    return state


async def ignore(state: AgentState, config: RunnableConfig) -> AgentState:
    """Ignore email (newsletter/promo) - MOCK version"""
    print("🗑️ Ignored email (newsletter/promo).")
    
    mail = state.get("mail")
    if mail:
        # UPDATED: Use mock mark_as_processed (no db needed)
        mark_as_processed(mail['id'])
        print(f"✅ [MOCK] Marked email {mail['id']} as read.")
        
    return state


async def notify_human(state: AgentState, config: RunnableConfig) -> AgentState:
    """Notify human about important email - MOCK version"""
    print("🔔 Notifying human: important email.")
    
    mail = state.get("mail")
    if mail:
        # UPDATED: Mock version - just log (no real Gmail label)
        print(f"✅ [MOCK] Labeled email {mail['id']} as AI-Notify")
        mark_as_processed(mail['id'])
        print(f"✅ [MOCK] Marked email {mail['id']} as read.")
        
    return state

def respond_act(state:AgentState)->AgentState:
    """Initiate ReAct Agent Loop"""
    print("🤖 Initiating React_Agent_Loop")
    return state

