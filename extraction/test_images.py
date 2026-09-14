import os
import glob
from agent import client, config, call_gemini, run_tool
from google.genai import types

sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_receipts")
image_files = (
    glob.glob(os.path.join(sample_dir, "*.jpeg"))
    + glob.glob(os.path.join(sample_dir, "*.jpg"))
    + glob.glob(os.path.join(sample_dir, "*.png"))
)

for image_path in image_files:
    print(f"\n--- Testing {os.path.basename(image_path)} ---")
    mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    contents = [
        types.Content(role="user", parts=[
            types.Part.from_text(text="Extract and save this receipt's data."),
            types.Part.from_bytes(data=image_bytes, mime_type=mime),
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
            types.Content(role="user", parts=[
                types.Part.from_function_response(name=part.function_call.name, response={"result": result})
            ])
        )
        response = call_gemini(contents, config)

    print(response.text)