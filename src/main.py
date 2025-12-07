from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

from langsmith import Client
client = Client()

llm = ChatOpenAI(
    model="gpt-4o-mini",
)

def hello_agent():
    response = llm.invoke("Hello, I am testing my agent setup.")
    print("Agent response:", response)

if __name__ == "__main__":
    hello_agent()
