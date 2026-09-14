from google.genai import types
extract_receipt_data = types.FunctionDeclaration(
    name="extract_receipt_data",
    description="Extract structured data from a receipt: vendor name, total amount, date, and category.",
    parameters={
        "type": "object",
        "properties": {
            "vendor": {"type": "string"},
            "amount": {"type": "number"},
            "date": {"type": "string"},
            "category": {"type": "string", "enum": ["food", "travel", "office", "other"]},
        },
        "required": ["vendor", "amount", "date", "category"],
    },
)

tools = types.Tool(function_declarations=[extract_receipt_data])
save_receipt = types.FunctionDeclaration(
    name="save_receipt",
    description="Save a validated receipt to the database.",
    parameters={
        "type": "object",
        "properties": {
            "vendor": {"type": "string"},
            "amount": {"type": "number"},
            "date": {"type": "string"},
            "category": {"type": "string"},
        },
        "required": ["vendor", "amount", "date", "category"],
    },
)
tools = types.Tool(function_declarations=[extract_receipt_data, save_receipt])