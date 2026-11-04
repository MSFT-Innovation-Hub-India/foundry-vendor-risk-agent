"""Smoke-test the deployed MCP server end to end: connect over streamable-HTTP,
list tools, and call two tools so the managed-identity DB path is exercised."""
import asyncio, os, sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("MCP_URL", "https://your-container-app.region.azurecontainerapps.io/mcp")


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])

            r = await session.call_tool("get_vendor_profile", {"vendor_id": 1003})
            print("\nget_vendor_profile(1003):")
            for c in r.content:
                print(getattr(c, "text", c))

            r = await session.call_tool("get_incident_history", {"vendor_id": 1003})
            print("\nget_incident_history(1003):")
            for c in r.content:
                print(getattr(c, "text", c))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("SMOKE TEST ERROR:", type(e).__name__, e)
        sys.exit(1)
