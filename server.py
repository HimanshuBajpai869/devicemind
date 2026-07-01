from mcp.server.fastmcp import FastMCP
from collector import AndroidCollector

collector = AndroidCollector()
mcp = FastMCP("DeviceMind")


@mcp.tool()
def device_status():
    """Return full device health snapshot"""
    return collector.get_status()


if __name__ == "__main__":
    mcp.run()
