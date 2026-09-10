import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# 1. Initialize the client
client = genai.Client()

# 2. Define the tool structure (Function Declaration)
ping_declaration = types.FunctionDeclaration(
    name="ping",
    description="A test tool that echoes back a message.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "message": {"type": "STRING"}
        },
        "required": ["message"],
    }
)

# Wrap declaration in a Tool object
ping_tool = types.Tool(function_declarations=[ping_declaration])

# 3. Configure Gemini with the tool
config = types.GenerateContentConfig(
    tools=[ping_tool]
)

# 4. Initial prompt asking Gemini to trigger the tool
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text(text="Please ping the message 'Hello from Phase 1!'")]
    )
]

print("Sending initial prompt to Gemini...")
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=contents,
    config=config
)

# 5. The Agent Loop
while True:
    part = response.candidates[0].content.parts[0]

    # Check if Gemini wants to call a function
    if not part.function_call:
        # If Gemini didn't ask for a tool call, it gave its final text response
        print("\nFinal Model Response:")
        print(response.text)
        break

    # If it DID call a tool, inspect what it asked for
    call = part.function_call
    print(f"\n[Gemini requested tool]: {call.name}")
    print(f"[Arguments]: {call.args}")

    # Execute our code for the tool
    if call.name == "ping":
        message_arg = call.args.get("message", "")
        tool_result = f"echo: {message_arg}"

    # Append Gemini's tool call request to the conversation history
    contents.append(response.candidates[0].content)

    # Append our tool execution response back to Gemini
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": tool_result}
                )
            ]
        )
    )

    print("\nSending tool result back to Gemini...")
    # Send the updated conversation back to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config
    )