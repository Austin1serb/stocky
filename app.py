"""Vercel ASGI entrypoint for the public Stocky MCP server."""

import os

from starlette.responses import JSONResponse
from starlette.routing import Route

from stocky_mcp import StockyServer


def _env_list(name, defaults):
    raw_value = os.getenv(name)
    if not raw_value:
        return defaults

    return [item.strip() for item in raw_value.split(",") if item.strip()]


server = StockyServer(
    stateless_http=True,
    allowed_hosts=_env_list(
        "STOCKY_ALLOWED_HOSTS",
        [
            "stocky-mcp.vercel.app",
            "127.0.0.1:*",
            "localhost:*",
        ],
    ),
    allowed_origins=_env_list(
        "STOCKY_ALLOWED_ORIGINS",
        [
            "https://chatgpt.com",
            "https://chat.openai.com",
            "https://platform.openai.com",
            "http://127.0.0.1:*",
            "http://localhost:*",
        ],
    ),
)
app = server.mcp.streamable_http_app()


async def health(_request):
    return JSONResponse({
        "name": "stocky",
        "transport": "streamable-http",
        "mcp_endpoint": "/mcp",
        "auth": "none",
    })


app.routes.insert(0, Route("/", health, methods=["GET"]))
