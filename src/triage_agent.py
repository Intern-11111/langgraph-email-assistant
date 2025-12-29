import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def triage_email(email_body):
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash",temperature = 0)
    
    # This is the "logic" your mentor is looking for
    prompt = ChatPromptTemplate.from_template("""
    You are an AI Email Assistant. Classify the following email into exactly one of these categories:
    - respond: If the email needs a draft reply or action.
    - notify_human: If it is urgent, personal, or contains a complex request.
    - ignore: If it is spam, a generic promotion, or doesn't need any action.
    
    Email: {email}
    
    Category:""")
    
    chain = prompt | llm
    response = chain.invoke({"email": email_body})
    return response.content.strip().lower()

# Test it
if __name__ == "__main__":
    test_email = "Claim your free $500 gift card now!"
    result = triage_email(test_email)
    print(f"Triage Result: {result}")