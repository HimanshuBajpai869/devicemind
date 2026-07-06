from mcp.server.fastmcp import FastMCP
from collector.collector import AndroidCollector

collector = AndroidCollector()
mcp = FastMCP("DeviceMind")


@mcp.tool()
def device_status():
    """Return full device health snapshot"""
    return collector.get_status()


@mcp.tool()
def battery_status():
    """Return device battery status health snapshot"""
    return collector.get_battery()


@mcp.tool()
def storage_status():
    """Return device storage status health snapshot"""
    return collector.get_storage()


if __name__ == "__main__":
    mcp.run()
