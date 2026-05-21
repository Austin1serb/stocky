"""Vercel ASGI entrypoint for the public Stocky MCP server."""

from starlette.responses import JSONResponse
from starlette.routing import Route

from stocky_mcp import StockyServer


server = StockyServer(stateless_http=True)
app = server.mcp.streamable_http_app()


async def health(_request):
    return JSONResponse({
        "name": "stocky",
        "transport": "streamable-http",
        "mcp_endpoint": "/mcp",
        "auth": "none",
    })


app.routes.insert(0, Route("/", health, methods=["GET"]))
