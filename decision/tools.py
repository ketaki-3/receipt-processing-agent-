from google.genai import types

check_budget = types.FunctionDeclaration(
    name="check_budget",
    description="Check whether a new expense would exceed the monthly budget for a category.",
    parameters={
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Expense category (e.g., food, travel)."},
            "amount": {"type": "number", "description": "Expense amount."},
        },
        "required": ["category", "amount"],
    },
)

check_duplicate = types.FunctionDeclaration(
    name="check_duplicate",
    description="Check if a very similar receipt (same vendor, amount, and date) already exists.",
    parameters={
        "type": "object",
        "properties": {
            "vendor": {"type": "string", "description": "Merchant name."},
            "amount": {"type": "number", "description": "Total amount paid."},
            "date": {"type": "string", "description": "Transaction date in YYYY-MM-DD format."},
        },
        "required": ["vendor", "amount", "date"],
    },
)

flag_anomaly = types.FunctionDeclaration(
    name="flag_anomaly",
    description="Check if an expense amount is unusually high compared to the category average.",
    parameters={
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Expense category."},
            "amount": {"type": "number", "description": "Expense amount to evaluate."},
        },
        "required": ["category", "amount"],
    },
)

save_receipt = types.FunctionDeclaration(
    name="save_receipt",
    description="Saves an approved receipt record into the receipts database.",
    parameters={
        "type": "object",
        "properties": {
            "vendor": {"type": "string", "description": "Merchant name."},
            "amount": {"type": "number", "description": "Total expense amount."},
            "date": {"type": "string", "description": "Transaction date in YYYY-MM-DD format."},
            "category": {"type": "string", "description": "Expense category (e.g., food, travel, office, other)."},
        },
        "required": ["vendor", "amount", "date", "category"],
    },
)

tools = [
    types.Tool(
        function_declarations=[
            check_budget,
            check_duplicate,
            flag_anomaly,
            save_receipt,
        ]
    )
]