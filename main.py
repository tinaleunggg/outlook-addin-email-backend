from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.classify import classify_email
from ai.analyze import summarize_email
from ai.response import generate_draft
import httpx
import asyncio

app = FastAPI()

# Enable CORS for your add-in
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your add-in URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailData(BaseModel):
    subject: str
    body: str


@app.get("/")
async def root():
    return {"message": "Hello from outlook add-in"}

@app.post("/api/analyze")
async def analyze_email(data: EmailData):
    email_body = data.body
    email_subject = data.subject
    
    try:
        async with httpx.AsyncClient() as client:
            classification, analysis = await asyncio.gather(
                classify_email(email_subject, email_body, client), 
                summarize_email(email_subject, email_body, client)
                )
            draft = await generate_draft(email_subject, email_body, analysis, client)
        
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

# for development use
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="localhost", port=5000, ssl_keyfile=r"C:\\Users\\tinal\\.office-addin-dev-certs\\localhost.key", ssl_certfile=r"C:\\Users\\tinal\\.office-addin-dev-certs\\localhost.crt")
    
