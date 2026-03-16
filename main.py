from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from openai import AzureOpenAI
# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
import os
from pydantic import BaseModel

from email_cleaner import clean_emails

from ai.classify import classify_email
from ai.analyze import summarize_email
from ai.response import generate_draft

app = FastAPI()

# Enable CORS for your add-in
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000",
        "http://localhost:3000",
        "https://127.0.0.1:3000",
        "http://127.0.0.1:3000",
                    ],  # Your add-in URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailData(BaseModel):
    subject: str
    body: str


# # Initialize Azure OpenAI
# azure_client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_KEY"),
#     api_version="2024-02-01",
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
# )

# # Initialize vector store for RAG
# embeddings = OpenAIEmbeddings(
#     deployment="text-embedding-ada-002",
#     openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
#     openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     openai_api_type="azure"
# )
# vectorstore = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embeddings
# )

@app.post("/api/analyze")
async def analyze_email(data: EmailData):
    email_body = data.body
    email_subject = data.subject
    
    try:
        classification = classify_email(email_subject, email_body)
        analysis = summarize_email(email_subject, email_body)
        draft = generate_draft(email_subject, email_body, analysis)
    
        return {
            "subject": email_subject,
            "body_clean": email_body,
            "category": classification.get("category"),
            "subcategory": classification.get("subcategory"),
            "confidence": classification.get("confidence"),
            "summary": analysis.get("summary"),
            "intent": analysis.get("intent"),
            "copilot_action": analysis.get("copilot_action"),
            "draft_reply": draft
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, ssl_keyfile=r"C:\\Users\\tinal\\.office-addin-dev-certs\\localhost.key", ssl_certfile=r"C:\\Users\\tinel\\.office-addin-dev-certs\\localhost.crt")
    
