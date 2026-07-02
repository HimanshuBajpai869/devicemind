from ollama import chat
import json

SYSTEM_PROMPT = """
You are the planner for an Android Device Assistant.

Available tools:

- device_status

Your job is ONLY to decide which tool should be called.

Return ONLY valid JSON.

Example:

{
  "tool":"device_status"
}
"""


class Planner:

    def plan(self, query: str):

        response = chat(
            model="qwen3:8b",
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

        text = response.message.content

        return json.loads(text)
