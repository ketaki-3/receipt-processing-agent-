from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="in one sentence, what do you think is the best career path at the moment?",
)
print(response.text)
for m in client.models.list():
       print(m.name)