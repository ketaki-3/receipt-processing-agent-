import os
from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents="In one sentence, what does a receipt-processing agent do?",
)
print(response.text)
