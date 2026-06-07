from fastmcp import FastMCP
from tools import create_user, update_user, get_user_by_id, get_users_by_date_range

mcp = FastMCP("User MCP Server")

mcp.tool()(create_user)
mcp.tool()(update_user)
mcp.tool()(get_user_by_id)
mcp.tool()(get_users_by_date_range)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)