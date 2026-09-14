from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools import tools

import sqlite3
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "receipts.db")

client = genai.Client()
config = types.GenerateContentConfig(tools=[tools])


def call_gemini(contents, config, retries=4, delay=8):
    for attempt in range(retries):
        try:
            return client.models.generate_content(model="gemini-flash-lite-latest", contents=contents, config=config)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise RuntimeError("Gemini API failed after multiple retries")


def run_tool(name, args):
    conn = sqlite3.connect(DB_PATH)

    if name == "extract_receipt_data":
        result = {"status": "extracted", **args}

    elif name == "save_receipt":
        conn.execute(
            "INSERT INTO receipts (vendor, amount, date, category) VALUES (?, ?, ?, ?)",
            (args["vendor"], args["amount"], args["date"], args["category"]),
        )
        conn.commit()
        result = {"status": "saved"}

    else:
        result = {"error": f"Unknown tool: {name}"}

    conn.close()
    return result


if __name__ == "__main__":
    image_path = os.path.join(os.path.dirname(__file__), "..", "sample_receipts", "receipt1.jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    contents = [
        types.Content(role="user", parts=[
            types.Part.from_text(text="Extract and save this receipt's data."),
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ])
    ]

    response = call_gemini(contents, config)

    while True:
        part = response.candidates[0].content.parts[0]
        if not part.function_call:
            break

        result = run_tool(part.function_call.name, dict(part.function_call.args))

        contents.append(response.candidates[0].content)
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=part.function_call.name, response={"result": result})],
            )
        )

        response = call_gemini(contents, config)

    print(response.text)