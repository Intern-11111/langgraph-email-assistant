from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # Specify the HuggingFace model repo
    task="text-generation"  
)
# Create a chat model using HuggingFace
model = ChatHuggingFace(llm=llm)

# Define a prompt template
template = PromptTemplate(
    template="give me a detailed explanation about {topic}",
    input_variables=["topic"]
)

# Output parser to convert model output to string
parser = StrOutputParser()

# Build the chain
chain = template | model | parser
output = chain.invoke({"topic": "AI"})  

print(output)

print("--------------------------------------------------------------------------------------------------------------------")

# Create a chat model using Google Generative AI
model2 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"  # Specify the Google Gemini model
)

# Build the chain: 
chain2 = template | model2 | parser
output2 = chain2.invoke({"topic": "hockey"})  
print(output2)