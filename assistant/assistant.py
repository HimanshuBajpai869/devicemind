from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class DeviceAssistant:

    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python3",
            args=["-m", "server.server"],
        )

    async def get_device_status(self):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("device_status", {})
                return result.content[0].text

    async def call_tool(self, tool_name: str):

        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(tool_name, {})

                return result.content[0].text
