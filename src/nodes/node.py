from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from pydantic import Field,BaseModel
from src.state import AgentState
from src.config import gemini_ai_model
from src.tools.tools import send_gmail_reply, read_calendar_availability, get_user_prefs,DANGEROUS_TOOLS,extract_meeting_from_email
from src.tools.calendar import IST,extract_event_details_llm,create_calendar_event
from src.hitl_handler import handle_hitl 
from typing import Literal,Annotated,Dict,Any,List
from langchain_core.output_parsers import PydanticOutputParser
from datetime import timedelta, timezone, datetime
#from langgraph.prebuilt import create_react_agent
# The function "create_react_agent" is deprecated
#   create_react_agent has been moved to `langchain.agents`. Please update your import to `from langchain.agents import create_agent`.
#from langchain.agents import create_agent
from langgraph.graph.message import add_messages
import re
import json

import time
from google.api_core import exceptions
model_gemini=gemini_ai_model()



class Category(BaseModel):
    category: Annotated[Literal["ignore","notify-human","respond-act"],"The classification of the email based on the rules."]

parser=PydanticOutputParser(pydantic_object=Category)
#  Subject: {subject}
#     Body: {body}
    
#     {format_instructions}  <-- ENSURE THIS IS INCLUDED

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
def triage_node(state:AgentState)->AgentState:
    mail=state['mail']

    chain=prompt|model_gemini|parser
    result_obj=chain.invoke({"subject":mail['subject'],"body":mail['body']})
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
    
# def react_route(state: AgentState):

#     if state.get("tool_name"):
#         return "react_tools"
#     elif state.get("final_reply"):
#         return "react_end"
#     else:
#         return "react_model"

def react_route(state: AgentState) -> str:
    # If we have a pending HITL envelope → go to checkpoint
    if state.get("hitl") and state.get("hitl_decision") == "pending":
        return "hitl_checkpoint"

    # If model is done → end
    if state.get("final_reply") and not state.get("tool_name"):
        return "react_end"

    # Safe tools only
    if state.get("tool_name"):
        # If tool_name is dangerous, don't route here; HITL will handle it
        if state["tool_name"] in DANGEROUS_TOOLS:
            return "hitl_checkpoint"
        return "react_tools"

    return "react_model"


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

def react_model_node(state: AgentState) -> AgentState:
    mail = state["mail"]
    messages: List[Any] = state.get("messages", []).copy()

    # 1) Build dynamic date context
    now_ist = datetime.now(IST)
    event_details = extract_event_details_llm(mail["body"], mail["subject"])

    date_context = f"""
    📅 LIVE DATE PARSING (IST):
    Today: {now_ist.strftime('%Y-%m-%d %A %H:%M')}
    LLM Extracted: {json.dumps(event_details) if event_details else 'None'}

    Slots parsed: {event_details.get('slots', []) if event_details else []}
    """

    # 2) System prompt
    react_prompt = f"""Production Email Assistant - FULL AUTONOMY

{date_context}

CRITICAL RULES:
1. DO NOT give a natural language "Final reply" until you have successfully called 
   send_gmail_reply or create_calendar.
2. After calling read_calendar_availability, you MUST immediately call create_calendar 
   (if free) or send_gmail_reply (if busy/to confirm).
3. If you stop without calling a dangerous tool, the workflow fails. STAY IN THE TOOL LOOP.
4. Do NOT provide a natural language 'Final reply' until you have called create_calendar or send_gmail_reply. 
   If a slot is free, your immediate next step MUST be to call create_calendar.

MANDATORY CHAINS:
1. MEETING: extract_meeting_from_email() → read_calendar_availability() → create_calendar() → send_gmail_reply()
2. REPLY: get_user_prefs() → send_gmail_reply()


🛡️ DANGEROUS (HITL):
- create_calendar(summary, start, end, location)
- send_gmail_reply(to, subject, body)

✅ SAFE:
- extract_meeting_from_email(subject, body)
- read_calendar_availability(start, end)
- get_user_prefs()


JSON ONLY:
{{"tool": "read_calendar_availability", "args": {{"start": "2026-01-03T14:00:00", "end": "2026-01-03T15:00:00"}}}}
"""

    # 3) Initialize messages for first turn
    if not messages:
        messages.append(SystemMessage(content=react_prompt))
        messages.append(
            HumanMessage(content=f"Subject: {mail['subject']}\nBody: {mail['body']}")
        )

    # 4) Call LLM with retry
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            resp = model_gemini.invoke(messages)
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

    text = resp.text
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

    # 8) No tool emitted → treat as final reply
    print("💬 Final reply (no tools)")
    messages.append(AIMessage(content=text))
    state["messages"] = messages
    state["final_reply"] = text
    state["tool_name"] = None
    state["tool_args"] = {}
    state["hitl"] = None
    state["hitl_decision"] = None
    return state    

def react_tools_node(state: AgentState) -> AgentState:
    tool_args = state.get("tool_args") or {}
    messages = state.get("messages", []).copy()
    tool_name = state.get("tool_name")

    result = None

    if tool_name == "read_calendar_availability":
        result = read_calendar_availability.invoke(tool_args)
    elif tool_name == "get_user_prefs":
        result = get_user_prefs.invoke(tool_args)
    elif tool_name == "extract_meeting_from_email":
        result = extract_meeting_from_email.invoke(tool_args)
    elif tool_name is None:
        result = "No tool to execute."
    else:
        # Dangerous or unknown tools should NOT be executed here
        result = f"Skipped execution of dangerous or unknown tool: {tool_name}"

    messages.append(HumanMessage(content=f"Tool '{tool_name}': {result}"))
    print(f"✅ Tool '{tool_name}' → {result}")

    # Clear tool_name/tool_args so react_route can decide next step
    state["messages"] = messages
    state["tool_name"] = None
    state["tool_args"] = None
    return state

def hitl_checkpoint(state: AgentState) -> AgentState:
    hitl = state.get("hitl") or {}
    decision = state.get("hitl_decision")
    tool_name = hitl.get("tool")
    tool_args = hitl.get("args") or {}

    if not tool_name:
        # Nothing to do, just continue the graph
        return state

    # DENY: do not execute tool
    if decision == "deny":
        denial_msg = HumanMessage(
            content="Human denied this action. Do not execute the tool."
        )
        state["messages"] = [denial_msg]
        state["final_reply"] = "Action denied by human."
        state["hitl"] = None
        state["hitl_decision"] = None  # optional, but keeps state clean
        state["tool_name"] = None
        state["tool_args"] = {}
        return state

    # APPROVE or EDIT: execute the tool with (possibly) edited args
    if decision in ("approve", "edit"):
        result: Any = None

        if tool_name == "send_gmail_reply":
            if hasattr(send_gmail_reply, "invoke"):
                result = send_gmail_reply.invoke(tool_args)
            else:
                result = send_gmail_reply(**tool_args)

        elif tool_name == "create_calendar":
            result = create_calendar_event(
                summary=tool_args.get("summary"),
                start_time=tool_args.get("start"),
                end_time=tool_args.get("end"),
                location=tool_args.get("location"),
            )

        # Add more dangerous tools here as needed

        confirm_text = (
            f"[{decision.upper()}] Executed tool {tool_name} "
            f"with args {tool_args}. Result: {result}"
        )
        state["messages"] = [HumanMessage(content=confirm_text)]
        state["final_reply"] = confirm_text
        state["hitl"] = None
        state["hitl_decision"] = None  # reset so future flows are clean
        state["tool_name"] = None
        state["tool_args"] = {}
        return state

    # If decision is still pending/None, just return state (graph should be suspended here)
    return state

def ignore(state:AgentState)->AgentState:
    print("Ignored email (newsletter/promo).")
    return state


def notify_human(state:AgentState)->AgentState:
    print("Notifying human: important email.")
    return state

def respond_act(state:AgentState)->AgentState:
    print("Initiating React_Agent_Loop")
    return state

