from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools import tools

client = genai.Client()
config = types.GenerateContentConfig(tools=[tools])

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="I bought coffee at Third Wave Coffee for ₹350 on 2026-08-10. Extract this as receipt data.",
    config=config,
)

part = response.candidates[0].content.parts[0]
if part.function_call:
    print("Tool called:", part.function_call.name)
    print("Arguments:", dict(part.function_call.args))
else:
    print("No tool was called. Gemini said:", response.text)