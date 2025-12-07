from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
	raise ValueError("OPENAI_API_KEY environment variable is not set")

chat = ChatOpenAI(temperature=0.5)

response = chat.invoke([HumanMessage(content="Hello! Can you introduce yourself?")])
print(response.content)
