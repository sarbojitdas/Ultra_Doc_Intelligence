import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = None

def get_client():
    global client

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    if client is None:
        client = Groq(api_key=api_key)

    return client


def llm_call(prompt):
    client = get_client()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content