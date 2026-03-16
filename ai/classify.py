from .ai_client import call_azure_openai
import json, re

CATEGORIES = {
    "Tenant Emails": [
        "Requests (maintenance, lease questions, move-in/out)",
        "Complaints (noise, neighbour, infractions)",
        "Payments (issues, confirmations)",
        "Applications / screening (new tenants, documents, credit checks)",
        "Renewal or termination requests",
        "General inquiries (amenities, building policies)"
    ],
    "Owner Emails": [
        "Approval requests (repairs, renewals)",
        "Updates & reports (financial, occupancy)",
        "General questions (income, expenses, property status)",
        "Property sale / transfer notices"
    ],
    "Finance & Accounting": [
        "Rent payment confirmations",
        "Late fee notices / collections",
        "Vendor invoices & receipts",
        "Utility bills, deposits, reimbursements",
        "Budget reports",
        "Tax documents or questions"
    ],
    "Operations & Vendors": [
        "Scheduling repairs/inspections",
        "Contractor coordination",
        "Emergencies (water damage, fire, break-ins)",
        "Quotes / bids from contractors",
        "Work completion confirmations"
    ],
    "Legal & Compliance": [
        "Lease agreements / renewals",
        "Eviction notices",
        "Insurance / liability issues",
        "Strata rule enforcement",
        "Rent increase notices",
        "Bylaw / legal disputes"
    ],
    "General / Announcements": [
        "Strata notices",
        "Community events / updates",
        "Manager bulletins or newsletters",
        "Meeting invites / acceptances",
        "General acknowledgements (thanks, confirmations)",
        "Out-of-office replies"
    ],
    "Internal / Staff": [
        "Staff scheduling / HR",
        "Internal policy updates",
        "Training / onboarding materials",
        "Team coordination"
    ],
    "Prospective Clients / Leads": [
        "Rental inquiries (new clients)",
        "Property viewing requests",
        "Pricing / availability questions",
        "Marketing / advertising responses"
    ],
    "System / Automated Messages": [
        "System errors / glitches",
        "Automated reminders (rent due, inspections)",
        "Bounce backs / delivery failures",
        "Subscription or account notifications"
    ]
}
async def classify_email(subject:str , body:str , client):
    categories_text = "\n".join([f"- {k}: {', '.join(v)}" for k,v in CATEGORIES.items()])
    
    prompt = f"""
    You are an email triage assistant for a property management company.
    Classify the following email into ONE main category and ONE subcategory from the list below. 
    You MUST always choose the closest matching category and subcategory, even if the email is vague. 
    Respond STRICTLY in valid JSON — no commentary, no extra text, no markdown, no explanations.

    Categories:
    {categories_text}

    Email:
    Subject: {subject}
    Body: {body[:3000]}

    Respond ONLY in JSON like this:
    {{
      "category": "<main category>",
      "subcategory": "<subcategory>",
      "confidence": <0-1>,
      "copilot_action": "<suggested action>"
    }}
    """
    raw = await call_azure_openai(prompt, client=client)


    # Try to safely extract JSON
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception as e:
            print("JSON parse failed:", e)
            return {"category": "System / Automated Messages", "subcategory": "Automated reminders (rent due, inspections)", "confidence": 0.3, "copilot_action": "Review manually"}

    # Fallback if nothing matched
    return {"category": "System / Automated Messages", "subcategory": "Automated reminders (rent due, inspections)", "confidence": 0.2, "copilot_action": "Review manually"}