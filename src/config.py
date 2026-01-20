#from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import os

# env_path = Path(__file__).parent.parent / ".env"

# load_dotenv(dotenv_path=env_path)

load_dotenv()
# def hugging_face_model()->ChatHuggingFace:

#     if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
#         raise ValueError("Error: HUGGINGFACEHUB_API_TOKEN not found in environment.")

#     llm = HuggingFaceEndpoint(
#         repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # Specify the HuggingFace model repo
#         #repo_id="google/gemma-2b-it",
#         task="text-generation",
#         max_new_tokens=128,
#         temperature=0.2

#     )

#     # Create a chat model using HuggingFace
#     model = ChatHuggingFace(llm=llm)
#     print("✅ LLM ready!")

#     return model


# Create a chat model using Google Generative AI
def gemini_ai_model()->ChatGoogleGenerativeAI:

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Error: GOOGLE_API_KEY not found in environment.")
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",  # Specify the Google Gemini model
         #google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    print("✅ LLM ready!")
    return model


# def open_ai_model()->ChatOpenAI:

#     model=ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0.3
#     )

#     return model