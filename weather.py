from mcp.server.fastmcp import FastMCP
# from mcp.types import Info, Tool

mcp = FastMCP("weather-mcp")

@mcp.tool()
def convert_temperature(celsius: float) -> float:
    return celsius * 9/5 + 32

if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
        print("Weather MCP is running on http://0.0.0.0:8000")
    except Exception as e:
        print(f"Error: {e}")
        