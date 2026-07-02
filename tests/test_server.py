import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters


async def main():

    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", tools)

            result = await session.call_tool("device_status", {})
            print("\nRESULT:\n", result)


asyncio.run(main())
