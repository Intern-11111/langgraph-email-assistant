from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os


class LLMFallbackTriage:

    def __init__(self):
        # Load .env so OPENAI_API_KEY is available if not set in system env
        load_dotenv()
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # The categories we allow
        self.allowed_labels = [
            "spam", "promotion", "finance", "meeting",
            "job_related", "transactional", "automated",
            "personal", "unknown"
        ]


    def classify(self, subject, body):   #Returns { label, confidence, source }
 
        prompt = ChatPromptTemplate.from_template("""
You are an email classifier. Read the email and respond ONLY in JSON.

Email subject: {subject}
Email body: {body}

Classify the email into one of these categories:
- spam
- promotion
- finance
- meeting
- job_related
- transactional
- automated
- personal
- unknown

Return JSON in this EXACT format:
{{
    "label": "one_of_the_categories",
    "confidence": number_between_0_and_1
}}

Think step-by-step internally but ONLY output JSON.
""")

        chain = prompt | self.model

        llm_response = chain.invoke({
            "subject": subject,
            "body": body
        })

        # Parse JSON safely
        try:
            result = eval(llm_response.content)
        except:
            # If LLM fails → default fallback
            result = {
                "label": "unknown",
                "confidence": 0.50
            }

        # Ensure valid label
        if result["label"] not in self.allowed_labels:
            result["label"] = "unknown"

        # Ensure confidence is in range
        conf = result.get("confidence", 0.5)
        conf = max(0, min(conf, 1))  

        return {
            "label": result["label"],
            "confidence": conf,
            "source": "llm"
        }


if __name__ == "__main__":
    triage = LLMFallbackTriage()

    subject = "Can we schedule a Zoom call tomorrow?"
    body = "Let me know your availability."

    print(triage.classify(subject, body))
