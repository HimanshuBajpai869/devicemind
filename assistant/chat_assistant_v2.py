import asyncio
from llm.agent import DeviceAgent


async def main():

    agent = DeviceAgent()

    print("📱 DeviceMind\n")

    while True:

        query = input("You: ")

        if query == "exit":
            break

        answer = await agent.chat(query)

        print("\nAssistant:\n")
        print(answer)
        print()


asyncio.run(main())
