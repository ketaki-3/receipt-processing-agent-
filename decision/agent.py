import os
import sqlite3
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from decision.tools import tools


def run_tool(name: str, args: dict) -> dict:
    conn = sqlite3.connect("receipts.db")
    cursor = conn.cursor()

    if name == "check_budget":
        category = args.get("category")
        amount = args.get("amount", 0)

        cursor.execute(
            "SELECT monthly_limit FROM budgets WHERE category = ?", (category,)
        )
        row = cursor.fetchone()
        limit = row[0] if row else None

        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM receipts WHERE category = ?",
            (category,),
        )
        spent = cursor.fetchone()[0]

        would_exceed = (spent + amount > limit) if limit is not None else False
        conn.close()
        return {
            "limit": limit,
            "already_spent": spent,
            "would_exceed_budget": would_exceed,
        }

    elif name == "check_duplicate":
        cursor.execute(
            "SELECT id FROM receipts WHERE vendor = ? AND amount = ? AND date = ?",
            (args.get("vendor"), args.get("amount"), args.get("date")),
        )
        row = cursor.fetchone()
        conn.close()
        return {"is_duplicate": row is not None}

    elif name == "flag_anomaly":
        category = args.get("category")
        amount = args.get("amount", 0)

        cursor.execute(
            "SELECT AVG(amount) FROM receipts WHERE category = ?", (category,)
        )
        row = cursor.fetchone()
        avg = row[0] if row and row[0] is not None else None

        is_anomaly = (amount > avg * 3) if avg is not None else False
        conn.close()
        return {
            "category_average": avg,
            "is_anomaly": is_anomaly,
        }

    elif name == "save_receipt":
        vendor = args.get("vendor")
        amount = args.get("amount")
        date = args.get("date")
        category = args.get("category")

        cursor.execute(
            "INSERT INTO receipts (vendor, amount, date, category) VALUES (?, ?, ?, ?)",
            (vendor, amount, date, category),
        )
        conn.commit()
        receipt_id = cursor.lastrowid
        conn.close()
        return {"status": "success", "saved_id": receipt_id}

    conn.close()
    return {"error": f"Unknown tool: {name}"}


load_dotenv()
client = genai.Client()


def run_agent(user_prompt: str):
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            tools=tools,
            system_instruction=(
                "You are an autonomous financial receipt processing agent. "
                "Execute the requested checks using your tools. "
                "Always end with an explicit, complete sentence explaining whether the receipt was approved and saved or rejected and why."
            ),
            temperature=0.1,
        ),
    )

    # Initial prompt submission with backoff retry for 503 errors
    response = None
    for attempt in range(3):
        try:
            response = chat.send_message(user_prompt)
            break
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 3
                print(f"Model busy (503). Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    # Tool invocation loop
    while response and response.function_calls:
        for fn_call in response.function_calls:
            tool_name = fn_call.name
            tool_args = dict(fn_call.args)
            print(f"-> Gemini requested tool: {tool_name} with {tool_args}")

            tool_output = run_tool(tool_name, tool_args)

            # Function response return with backoff retry for 503 errors
            for attempt in range(3):
                try:
                    response = chat.send_message(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={"result": tool_output},
                        )
                    )
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < 2:
                        wait_time = (attempt + 1) * 3
                        print(f"Model busy (503). Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e

    if response:
        print("\nFinal Answer:\n", response.text)


if __name__ == "__main__":
    prompt = (
        "Process this incoming expense:\n"
        "Vendor: Blue Tokai\n"
        "Amount: 420.0\n"
        "Date: 2026-08-10\n"
        "Category: food\n\n"
        "Instructions:\n"
        "1. Check if this is a duplicate.\n"
        "2. Check if it would exceed our food budget.\n"
        "3. Check if this amount is an anomaly.\n"
        "4. If all checks pass, save the receipt using the save_receipt tool. "
        "If any check fails, do NOT save and explain why."
    )
    run_agent(prompt)