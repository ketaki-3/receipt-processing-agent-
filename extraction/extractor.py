import json
import os
import time
import warnings
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
client = genai.Client()

RECEIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {
            "type": "string",
            "description": "Store or merchant name on the receipt",
        },
        "amount": {
            "type": "number",
            "description": "Final total amount charged as a float or int",
        },
        "date": {
            "type": "string",
            "description": "Transaction date in YYYY-MM-DD format",
        },
        "category": {
            "type": "string",
            "description": "Expense category (food, travel, office, utilities, or other)",
        },
    },
    "required": ["vendor", "amount", "date", "category"],
}


def extract_receipt(image_path: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    image = Image.open(image_path)

    prompt = (
        "Analyze this receipt image. Extract the merchant/vendor name, "
        "the total final amount, transaction date, and infer a clean category "
        "(food, travel, office, utilities, or other)."
    )

    # Retry loop to handle brief 503 capacity spikes smoothly
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[image, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RECEIPT_SCHEMA,
                    temperature=0.1,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                print("Model busy (503). Retrying in 2 seconds...")
                time.sleep(2)
            else:
                raise e


if __name__ == "__main__":
    result = extract_receipt("sample_receipt.png")
    print("\nExtracted Data:")
    print(json.dumps(result, indent=2))