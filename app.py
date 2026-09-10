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
from extraction.extractor import extract_receipt
from decision.agent import client, tools, types, run_tool

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
        # Step 1: Multimodal OCR
        print(f"\n[1/3] Extracting metadata from {file.filename}...")
        data = extract_receipt(temp_path)
        print(f"Extracted payload: {data}")
        
        if not data:
            return JSONResponse(
                status_code=400,
                content={"detail": "Multimodal OCR failed to parse receipt."}
            )

        # Pause to prevent hitting the 5 RPM ceiling
        time.sleep(2)

        # Step 2: Agent Tool-Calling Loop
        prompt = (
            f"Process this incoming expense:\n"
            f"Vendor: {data.get('vendor')}\nAmount: {data.get('amount')}\nDate: {data.get('date')}\nCategory: {data.get('category')}\n\n"
            f"Instructions:\n"
            f"1. Check if this is a duplicate.\n"
            f"2. Check if it would exceed our {data.get('category')} budget.\n"
            f"3. Check if this amount is an anomaly.\n"
            f"4. If all checks pass, save the receipt using save_receipt. If any check fails, do NOT save and explain why."
        )

        print("[2/3] Calling Gemini agent decision loop...")
        chat = client.chats.create(
            model="gemini-3.6-flash",
            config=types.GenerateContentConfig(
                tools=tools,
                temperature=0.1,
                system_instruction="You are an autonomous financial auditor. Run requested tools sequentially. State final verdict.",
            ),
        )

        response = chat.send_message(prompt)
        checks_log = []

        while response and response.function_calls:
            for fn in response.function_calls:
                tool_name = fn.name
                tool_args = dict(fn.args)
                print(f" -> Executing Tool: {tool_name} with args: {tool_args}")
                tool_output = run_tool(tool_name, tool_args)

                is_fail = any(w in str(tool_output).lower() for w in ["error", "exceeded", "duplicate found", "fail"])
                checks_log.append({
                    "tool": tool_name,
                    "result": str(tool_output),
                    "passed": not is_fail,
                })

                time.sleep(1.5)  # Guardrail spacing for rate limits
                response = chat.send_message(
                    types.Part.from_function_response(name=tool_name, response={"result": tool_output})
                )

        verdict_text = response.text if response else "Audit complete."
        is_rejected = any(w in verdict_text.lower() for w in ["rejected", "not saved", "duplicate", "exceed", "failed"])

        print("[3/3] Audit completed successfully.")
        return {
            "status": "REJECTED" if is_rejected else "APPROVED",
            "extracted": data,
            "checks": checks_log,
            "verdict": verdict_text,
        }

    except ClientError as ce:
        print("\n--- GEMINI API QUOTA / RATE LIMIT ERROR ---")
        traceback.print_exc()
        return JSONResponse(
            status_code=429,
            content={"detail": "Gemini API rate limit reached (5 requests/min). Please wait 15 seconds and re-try."}
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