import os, json
from pathlib import Path
from dotenv import load_dotenv
# Get the directory where this file is located
current_dir = Path(__file__).parent.parent
env_path = current_dir / '.env'

# Load from specific path
load_dotenv(dotenv_path=env_path)

AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
DEPLOYMENT = os.getenv("DEPLOYMENT")


async def call_azure_openai(prompt, client=None, response_format=None, temperature=0):
    """Generic helper to call Azure OpenAI Chat Completion"""
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if response_format:
        payload["response_format"] = response_format

    url = f"{AOAI_ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version=2024-12-01-preview"
    r = await client.post(url, headers={"api-key": AOAI_KEY, "Content-Type": "application/json"}, json=payload)

    if r.status_code != 200:
        print("Azure OpenAI Error:", r.status_code, r.text)
        return None

    try:
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Response parsing error:", e)
        return None



if __name__ == "__main__":
    print(env_path)
    print(AOAI_ENDPOINT)
    print(AOAI_KEY)
    print(DEPLOYMENT)