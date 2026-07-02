from urllib import response

from ollama import chat
import json

MODEL = "tinyllama"

SYSTEM_PROMPT = """
You are a tool planner for DeviceMind.

Your ONLY responsibility is selecting the correct tool.

Available tools:

- device_status

Rules:

- Return one JSON object.
- Do not explain.
- Do not use markdown.
- Do not include any text before or after the JSON.

Example:

{"tool":"device_status"}
"""


class LLM:

    def planner(self, query: str):
        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )

        print("========== RAW LLM OUTPUT ==========")
        print(response.message.content)
        print("====================================")

        try:
            return json.loads(response.message.content)
        except Exception:
            print("⚠️ Planner returned invalid JSON. Falling back to device_status.")
            return {"tool": "device_status"}

    def reason(self, question: str, telemetry: dict):

        prompt = f"""
You are an Android device expert.

Question:

{question}

Telemetry:

{json.dumps(telemetry, indent=2)}

Answer naturally.

Do not invent values.

Use only supplied telemetry.
"""

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content
