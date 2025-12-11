from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from pydantic import Field,BaseModel
from state import AgentState
from config import hugging_face_model
from typing import Literal,Annotated
from langchain_core.output_parsers import PydanticOutputParser
#3from langchain.output_parsers import OutputFixingParser


model=hugging_face_model()

class Category(BaseModel):
    category: Annotated[Literal["ignore","notify-human","respond-act"],"The classification of the email based on the rules."]

parser=PydanticOutputParser(pydantic_object=Category)

prompt = PromptTemplate(template="""
You are an email triage assistant. Classify this email into EXACTLY ONE category:

- "ignore": Newsletters, promotions, auto-notifications (no action needed)
- "notify-human": Urgent issues, security alerts, executive comms, approvals
- "respond-act": Meetings, requests, reviews, questions that need reply/action

Email:
Subject: {subject}
Body: {body}

\n {format_instructions}
""",
input_variables=["subject", "body"],
    
partial_variables={"format_instructions": parser.get_format_instructions()}
)


#fixed_parser = OutputFixingParser.from_llm(parser=parser, llm=model)



# node function
def triage_node(state:AgentState)->AgentState:
    mail=state['mail']

    chain=prompt|model|parser
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
    

def ignore(state:AgentState)->AgentState:
    
    pass


def notify_human(state:AgentState)->AgentState:
    pass


def respond_act(state:AgentState)->AgentState:
    pass

