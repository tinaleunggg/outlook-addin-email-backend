import re
from bs4 import BeautifulSoup # type: ignore

def clean_html_email(content: str) -> str:

    if not content:
        return ""

    if "<" in content and ">" in content:
        soup = BeautifulSoup(content, "html.parser")


        for block in soup.find_all(["blockquote", "div"], {"class": ["gmail_quote", "yahoo_quoted"]}):
            block.decompose()

        for tag in soup(["style", "script"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
    else:
        text = content
    
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    reply_pattern = r"(?im)^(From:|On .+wrote:)"
    parts = re.split(reply_pattern, text)
    if parts:
        text = parts[0].strip()


    signature_patterns = [
        r"(?i)^sent from my iphone.*",
        r"(?i)^sent from outlook.*",
        r"(?i)^best regards.*",
        r"(?i)^kind regards.*",
        r"(?i)^cheers.*",
        r"(?i)^thanks(,|\.|!| )?.*",
        r"(?i)^regards.*",
        r"(?i)^david k\.? wong.*",
        r"(?i)^dk rentals.*"
    ]

    for p in signature_patterns:
        text = re.sub(p, "", text)


    text = re.sub(r"\s{2,}", " ", text).strip()
    return text

# def clean_emails(email_tuples):
#     cleaned = []
#     for subject, body_html in email_tuples:
#         cleaned_body = clean_html_email(body_html)
#         cleaned.append({
#             "subject": subject,
#             "body_clean": cleaned_body
#         })
#     return cleaned

def clean_emails(email_tuples):
    cleaned = []
    for item in email_tuples:
        # Graph path: (message_id, subject, body_html)
        if len(item) == 3:
            message_id, subject, body_html = item
        else:
            # mbox / legacy path: (subject, body_html)
            message_id = None
            subject, body_html = item

        cleaned_body = clean_html_email(body_html)
        cleaned.append({
            "message_id": message_id,
            "subject": subject,
            "body_clean": cleaned_body,
        })
    return cleaned

# ------------ this is for testing
if __name__ == "__main__":

    example_html = """
    <html>
      <body>
        <div>Hi David,<br><br>
        Just confirming I paid rent today.<br><br>
        Thanks,<br>John Smith<br>Sent from my iPhone</div>
      </body>
    </html>
    """

    result = clean_html_email(example_html)
    print("Cleaned Email:")
    print(result)
