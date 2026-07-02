from ollama import chat
import json

SYSTEM_PROMPT = """
You are an Android device expert.

You will receive:

1. User question
2. Device JSON

Answer naturally.

Do NOT invent values.

Only use supplied telemetry.
"""


class Reasoner:

    def answer(self, question: str, data: dict):

        response = chat(
            model="qwen3:8b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"""
Question:

{question}

Telemetry:

{json.dumps(data, indent=2)}
""",
                },
            ],
        )

        return response.message.content
