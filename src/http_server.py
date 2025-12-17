#!/usr/bin/env python3
"""
HTTP Server wrapper for JDE E1 MCP Server
Provides HTTP/SSE transport for Railway deployment
"""

import asyncio
import json
import os
from typing import Any
from aiohttp import web
import logging

from .server import server
from .knowledge_base import INSTALLATION_PREREQUISITES, INSTALLATION_SEQUENCE
from .environment_config import ENVIRONMENT_CONFIG, CENTRALIZED_CONFIGURATION, SERVER_MANAGER_CONFIG, ESU_ASU_REQUIREMENTS
from .troubleshooting import TROUBLESHOOTING_GUIDE, LOG_ANALYSIS, CONFIGURATION_UTILITIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jde-e1-http")

# Store for active sessions
sessions = {}

async def health_check(request: web.Request) -> web.Response:
    """Health check endpoint for Railway."""
    return web.json_response({
        "status": "healthy",
        "service": "jde-e1-config-mcp",
        "version": "1.0.0",
        "tools": 12,
        "resources": 7,
        "prompts": 4
    })

async def list_tools_handler(request: web.Request) -> web.Response:
    """List available MCP tools."""
    tools = await server.list_tools()
    return web.json_response({
        "tools": [{
            "name": t.name,
            "description": t.description,
            "inputSchema": t.inputSchema
        } for t in tools]
    })

async def list_resources_handler(request: web.Request) -> web.Response:
    """List available MCP resources."""
    resources = await server.list_resources()
    return web.json_response({
        "resources": [{
            "uri": r.uri,
            "name": r.name,
            "mimeType": r.mimeType
        } for r in resources]
    })

async def list_prompts_handler(request: web.Request) -> web.Response:
    """List available MCP prompts."""
    prompts = await server.list_prompts()
    return web.json_response({
        "prompts": [{
            "name": p.name,
            "description": p.description,
            "arguments": [{
                "name": a.name,
                "required": a.required
            } for a in (p.arguments or [])]
        } for p in prompts]
    })

async def call_tool_handler(request: web.Request) -> web.Response:
    """Call an MCP tool."""
    try:
        data = await request.json()
        tool_name = data.get("name")
        arguments = data.get("arguments", {})
        
        if not tool_name:
            return web.json_response({"error": "Missing tool name"}, status=400)
        
        result = await server.call_tool(tool_name, arguments)
        return web.json_response({
            "result": [{
                "type": r.type,
                "text": r.text
            } for r in result]
        })
    except Exception as e:
        logger.error(f"Error calling tool: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def read_resource_handler(request: web.Request) -> web.Response:
    """Read an MCP resource."""
    try:
        uri = request.query.get("uri")
        if not uri:
            return web.json_response({"error": "Missing URI parameter"}, status=400)
        
        result = await server.read_resource(uri)
        return web.json_response({"content": json.loads(result)})
    except Exception as e:
        logger.error(f"Error reading resource: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def get_prompt_handler(request: web.Request) -> web.Response:
    """Get an MCP prompt."""
    try:
        data = await request.json()
        name = data.get("name")
        arguments = data.get("arguments", {})
        
        if not name:
            return web.json_response({"error": "Missing prompt name"}, status=400)
        
        result = await server.get_prompt(name, arguments)
        return web.json_response({
            "description": result.description,
            "messages": [{
                "role": m.role,
                "content": m.content.text if hasattr(m.content, 'text') else str(m.content)
            } for m in result.messages]
        })
    except Exception as e:
        logger.error(f"Error getting prompt: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def index_handler(request: web.Request) -> web.Response:
    """Root endpoint with API documentation."""
    return web.json_response({
        "name": "JDE E1 9.2 R24 Configuration Research MCP",
        "version": "1.0.0",
        "description": "MCP Server for JD Edwards EnterpriseOne 9.2 Release 24 system configuration research",
        "endpoints": {
            "GET /": "This documentation",
            "GET /health": "Health check",
            "GET /tools": "List available tools",
            "GET /resources": "List available resources",
            "GET /prompts": "List available prompts",
            "POST /tools/call": "Call a tool (body: {name, arguments})",
            "GET /resources/read?uri=...": "Read a resource",
            "POST /prompts/get": "Get a prompt (body: {name, arguments})"
        },
        "environments": ["PD920 (Production)", "PY920 (Test)", "DV920 (Development)"],
        "tools_count": 12,
        "resources_count": 7,
        "prompts_count": 4
    })

def create_app() -> web.Application:
    """Create the aiohttp application."""
    app = web.Application()
    
    # Add routes
    app.router.add_get("/", index_handler)
    app.router.add_get("/health", health_check)
    app.router.add_get("/tools", list_tools_handler)
    app.router.add_get("/resources", list_resources_handler)
    app.router.add_get("/prompts", list_prompts_handler)
    app.router.add_post("/tools/call", call_tool_handler)
    app.router.add_get("/resources/read", read_resource_handler)
    app.router.add_post("/prompts/get", get_prompt_handler)
    
    return app

def main():
    """Run the HTTP server."""
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    logger.info(f"Starting JDE E1 MCP HTTP Server on port {port}")
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
