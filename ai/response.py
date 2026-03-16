from .ai_client import call_azure_openai

def generate_draft(subject, body, analysis):
    summary = analysis.get("summary", "")
    intent = analysis.get("intent", "")
    action = analysis.get("copilot_action", "")

    prompt = f"""
    You are a professional assistant for a property management company.
    Write a short (3–5 sentences) polite draft reply to the following email.

    Summary: {summary}
    Intent: {intent}
    Recommended Action: {action}

    Email:
    Subject: {subject}
    Body: {body[:2000]}

    Reply ONLY with the draft email text.
    Do NOT include any HTML tags. The reply must be plain text only.
    """
    return call_azure_openai(prompt)
