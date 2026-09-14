import os
import time
import sqlite3
import tempfile
import pathlib
import traceback
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from google.genai.errors import ClientError
from agent import client, run_tool
from tools import tools
from google.genai import types

app = FastAPI(title="Tabby Expense Copilot")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/api/ledger")
def get_ledger():
    try:
        conn = sqlite3.connect("receipts.db")
        c = conn.cursor()
        c.execute("SELECT id, vendor, amount, date, category FROM receipts ORDER BY id DESC")
        rows = c.fetchall()
        c.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM receipts")
        total_count, total_spend = c.fetchone()
        conn.close()
        return {
            "metrics": {"total_count": total_count, "total_spend": total_spend},
            "transactions": [
                {"id": r[0], "vendor": r[1], "amount": r[2], "date": r[3], "category": r[4]}
                for r in rows
            ],
        }
    except Exception as e:
        return {"metrics": {"total_count": 0, "total_spend": 0}, "transactions": []}

@app.post("/api/audit")
async def audit_receipt(file: UploadFile):
    ext = pathlib.Path(file.filename).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        temp_path = tmp.name

    try:
        with open(temp_path, "rb") as f:
            image_bytes = f.read()

        mime = "image/png" if ext.lower() == ".png" else "image/jpeg"

        print("[1/2] Sending receipt to agent for extraction + decision...")
        chat = client.chats.create(
            model="gemini-flash-lite-latest",
            config=types.GenerateContentConfig(
                tools=tools,
                temperature=0.1,
                system_instruction=(
                    "You are an autonomous financial receipt processing agent. "
                    "First extract the receipt's data, then check for duplicates, budget, and anomalies. "
                    "Always end with an explicit, complete sentence explaining whether the receipt was approved and saved or rejected and why."
                ),
            ),
        )

        response = chat.send_message([
            "Extract this receipt's data, then run all checks and save if appropriate.",
            types.Part.from_bytes(data=image_bytes, mime_type=mime),
        ])

        checks_log = []
        extracted_data = {}

        while response and response.function_calls:
            for fn in response.function_calls:
                tool_name = fn.name
                tool_args = dict(fn.args)
                print(f" -> Executing Tool: {tool_name} with args: {tool_args}")
                tool_output = run_tool(tool_name, tool_args)

                if tool_name == "extract_receipt_data":
                    extracted_data = tool_args

                is_fail = any(w in str(tool_output).lower() for w in ["error", "exceeded", "duplicate found", "fail"])
                checks_log.append({
                    "tool": tool_name,
                    "result": str(tool_output),
                    "passed": not is_fail,
                })

                time.sleep(1.5)
                response = chat.send_message(
                    types.Part.from_function_response(name=tool_name, response={"result": tool_output})
                )

        verdict_text = response.text if response else "Audit complete."
        is_rejected = any(w in verdict_text.lower() for w in ["rejected", "not saved", "duplicate", "exceed", "failed"])

        print("[2/2] Audit completed successfully.")
        return {
            "status": "REJECTED" if is_rejected else "APPROVED",
            "extracted": extracted_data,
            "checks": checks_log,
            "verdict": verdict_text,
        }

    except ClientError as ce:
        print("\n--- GEMINI API QUOTA / RATE LIMIT ERROR ---")
        traceback.print_exc()
        return JSONResponse(
            status_code=429,
            content={"detail": "Gemini API rate limit reached. Please wait and re-try."}
        )
    except Exception as e:
        print("\n--- BACKEND EXCEPTION ---")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Backend Error: {str(e)}"}
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)