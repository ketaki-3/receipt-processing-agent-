import sys
from decision.agent import run_agent
from extraction.extractor import extract_receipt


def process_receipt_image(image_path: str):
    print(f"\n--- 1. Extracting data from: {image_path} ---")
    data = extract_receipt(image_path)
    print(f"Extracted: {data}")

    prompt = (
        f"Process this incoming expense:\n"
        f"Vendor: {data['vendor']}\n"
        f"Amount: {data['amount']}\n"
        f"Date: {data['date']}\n"
        f"Category: {data['category']}\n\n"
        f"Instructions:\n"
        f"1. Check if this is a duplicate.\n"
        f"2. Check if it would exceed our {data['category']} budget.\n"
        f"3. Check if this amount is an anomaly.\n"
        f"4. If all checks pass, save the receipt using the save_receipt tool. "
        f"If any check fails, do NOT save and explain why."
    )

    print("\n--- 2. Running Autonomous Decision Agent ---")
    run_agent(prompt)


if __name__ == "__main__":
    target_image = "sample_receipt.png"
    if len(sys.argv) > 1:
        target_image = sys.argv[1]

    process_receipt_image(target_image)