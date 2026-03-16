from .ai_client import call_azure_openai
import json
import requests

def summarize_email(subject, body, classification=None):
    """
    Generates a summary and identifies the sender's intent.
    """

    category_hint = ""
    if classification and classification.get("category"):
        category_hint = f"This email was classified as '{classification['category']}' under subcategory '{classification.get('subcategory', '')}'."

    prompt = f"""
    You are an assistant for a property management company.
    Your task is to analyze the following email and extract:
    1. A short 1-2 sentence summary of the main content.
    2. The sender's intent (what they are asking, informing, or requesting).
    3. A helpful next action or recommendation for the Copilot.

    {category_hint}

    Email:
    Subject: {subject}
    Body: {body[:4000]}

    Respond ONLY in JSON like this:
    {{
      "summary": "<short summary>",
      "intent": "<sender's intent>",
      "copilot_action": "<recommended action>"
    }}
    """
    raw = call_azure_openai(prompt, response_format={"type": "json_object"})
    try:
        return json.loads(raw)
    except:
        return {"summary": "", "intent": "", "copilot_action": "Check manually"}