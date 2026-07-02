import json

from llm.llm import LLM
from assistant.assistant import DeviceAssistant


class DeviceAgent:

    def __init__(self):

        self.llm = LLM()
        self.device = DeviceAssistant()

    async def chat(self, query):

        print("🧠 Planning...")

        plan = self.llm.planner(query)

        print(plan)

        tool = plan["tool"]

        print(f"🔧 Calling {tool}")

        raw = await self.device.call_tool(tool)

        telemetry = json.loads(raw)

        print("🤖 Reasoning...")

        return self.llm.reason(query, telemetry)
