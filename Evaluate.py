import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

#Defining the 'Agent Quality Score' Metrics
class AgentQualityScore(BaseModel):
    helpfulness: int = Field(description="Score 1-5: Did it solve the user's intent?")
    tone: int = Field(description="Score 1-5: Was the language professional/appropriate?")
    accuracy: int = Field(description="Score 1-5: Is the response factually correct?")
    reasoning: str = Field(description="Brief explanation for the scores")
    is_pass: bool = Field(description="Overall Pass/Fail based on the rubric")

# Setting up the OpenAI Judge LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 4. Defining the Rubric
JUDGE_PROMPT = """
You are an AI Quality Judge. Grade the following Agent response based on the rubric.

- 5 (Excellent): Perfectly meets all criteria.
- 3 (Average): Correct but has minor tone issues or lacks conciseness.
- 1 (Poor): Wrong information, rude tone, or fails to help.

### Pass/Fail Criteria:
- Pass if ALL scores are 4 or higher.

### Inputs:
User Query: {user_input}
Agent Response: {agent_response}
"""

def evaluate_my_agent(query, response):
    judge_chain = llm.with_structured_output(AgentQualityScore)
    
    prompt = ChatPromptTemplate.from_template(JUDGE_PROMPT)
    chain = prompt | judge_chain
    
    return chain.invoke({
        "user_input": query,
        "agent_response": response
    })

if __name__ == "__main__":
    u_query = "Help me refund my order #1234. I'm very angry about the delay."
    a_reply = "I am sorry to hear about the delay. I have initiated a refund for order #1234. You should see it in 3 days."

    try:
        report = evaluate_my_agent(u_query, a_reply)

        print(f"--- OpenAI Quality Report ---")
        print(f"Helpfulness: {report.helpfulness}/5")
        print(f"Tone:        {report.tone}/5")
        print(f"Accuracy:    {report.accuracy}/5")
        print(f"Result:      {'PASS' if report.is_pass else 'FAIL'}")
        print(f"Reasoning:   {report.reasoning}")
    except Exception as e:
        print(f"Error during evaluation: {e}")