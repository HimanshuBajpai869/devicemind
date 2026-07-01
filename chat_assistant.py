import asyncio
from assistant import DeviceAssistant, format_response


class ChatDeviceAssistant:

    def __init__(self):
        self.assistant = DeviceAssistant()

    def decide_tool(self, query: str) -> str:
        q = query.lower()

        if "battery" in q:
            return "device_status"

        if "storage" in q:
            return "device_status"

        if "device" in q or "health" in q:
            return "device_status"

        return "device_status"

    def extract_fields(self, query: str):

        q = query.lower()

        fields = []

        if "battery" in q:
            fields.append("battery")

        if "storage" in q:
            fields.append("storage")

        if "device" in q or "model" in q:
            fields.append("device")

        if not fields:
            fields = ["device", "battery", "storage"]

        return fields

    async def handle_query(self, query: str):

        tool = self.decide_tool(query)

        raw = await self.assistant.call_tool(tool)

        fields = self.extract_fields(query)

        return format_response(raw, fields)


async def main():

    chat = ChatDeviceAssistant()

    print("📱 DeviceMind Assistant Ready")
    print("Type 'exit' to quit\n")

    while True:

        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            break

        response = await chat.handle_query(query)

        print("\nAssistant:\n", response)


asyncio.run(main())
