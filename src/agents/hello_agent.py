from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(openai_api_key=OPENAI_KEY, temperature=0.5)

response = chat([HumanMessage(content="Hello! Can you introduce yourself?")])
print(response.content)
