from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv("../.env")


def get_context(question: str) -> dict:
    print(question)
    # query the qdrant vector store for the context
    return "This is the context for the question :"

def get_system_prompt():
    return open("../prompt/manager.md").read()

client = genai.Client()

tools = [get_context]

config = types.GenerateContentConfig(tools=tools)

question = "What is the best health insurance policy for me?"
messages = [
    types.Content(role="model", parts=[types.Part.from_text(text=get_system_prompt())]),
    types.Content(role="user", parts=[types.Part.from_text(text=question)])
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=config,
)
print(response.text)
