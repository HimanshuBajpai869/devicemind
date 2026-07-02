import asyncio
from assistant import DeviceAssistant, format_response


async def main():

    assistant = DeviceAssistant()

    raw = await assistant.get_device_status()

    print(format_response(raw))


asyncio.run(main())
