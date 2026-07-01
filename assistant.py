import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class DeviceAssistant:

    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python3",
            args=["server.py"],
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


import json


def safe_parse(raw_text: str):
    try:
        return json.loads(raw_text)
    except Exception:
        return None


def format_response(raw_text: str, fields):

    data = safe_parse(raw_text)

    if not data:
        return "⚠️ Unable to read device data."

    device = data["device"]
    battery = data["battery"]
    storage = data["storage"]

    insights = []

    output = []

    if "device" in fields:
        output.append(f"📱 Device: {device['model']} ({device['android_version']})")

    if "battery" in fields:
        output.append(f"🔋 Battery: {battery['percentage']}% - {battery['status']}")
        output.append(f"🌡 Temperature: {battery['temperature']}°C")

    if "storage" in fields:
        output.append(
            f"💾 Storage: {storage['used_gb']:.1f}/{storage['total_gb']:.1f} GB used"
        )

    # insights always
    if battery["percentage"] < 30:
        insights.append("Battery is low.")
    if battery.get("charging"):
        insights.append("Phone is charging.")

    return (
        "\n".join(output)
        + "\n\n🧠 Insights:\n- "
        + ("\n- ".join(insights) if insights else "Everything looks normal.")
    )


# def format_response(raw_text: str) -> str:
#     data = json.loads(raw_text)

#     data = safe_parse(raw_text)

#     if not data:
#         return "⚠️ Unable to read device data right now."

#     device = data["device"]
#     battery = data["battery"]
#     storage = data["storage"]

#     print(battery)

#     insights = []

#     # Battery insight
#     if battery["percentage"] < 30:
#         insights.append("Battery is low.")
#     elif battery["status"] == "Charging":
#         insights.append("Phone is currently charging.")

#     # Temperature insight
#     if battery["temperature"] > 38:
#         insights.append("Device is running hot.")

#     # Storage insight
#     free_percent = (storage["available_gb"] / storage["total_gb"]) * 100
#     if free_percent < 15:
#         insights.append("Storage is running low.")

#     return f"""
# 📱 Device: {device['model']} ({device['android_version']})

# 🔋 Battery: {battery['percentage']}% - {battery['status']}
# 🌡 Temperature: {battery['temperature']}°C
# 💾 Storage: {storage['used_gb']:.1f}/{storage['total_gb']:.1f} GB used

# 🧠 Insights:
# - {chr(10).join(insights) if insights else "Everything looks normal."}
# """
