#!/usr/bin/env python3
"""
HTTP Server wrapper for JDE E1 MCP Server
Provides HTTP/REST API for Railway deployment
"""

import json
import os
import logging
from aiohttp import web

# Import knowledge base data directly
from .knowledge_base import INSTALLATION_PREREQUISITES, INSTALLATION_SEQUENCE
from .environment_config import (
    ENVIRONMENT_CONFIG,
    CENTRALIZED_CONFIGURATION,
    SERVER_MANAGER_CONFIG,
    ESU_ASU_REQUIREMENTS,
)
from .troubleshooting import (
    TROUBLESHOOTING_GUIDE,
    LOG_ANALYSIS,
    CONFIGURATION_UTILITIES,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jde-e1-http")

# Tool definitions
TOOLS = [
    {"name": "research_installation_prerequisites", "description": "Get prerequisites for JDE components"},
    {"name": "get_installation_sequence", "description": "Get installation sequence for environments"},
    {"name": "get_environment_configuration", "description": "Get environment config (PD920, PY920, DV920)"},
    {"name": "research_server_manager_config", "description": "Get Server Manager configuration"},
    {"name": "get_centralized_configuration_guide", "description": "Get Release 24 Centralized Configuration guide"},
    {"name": "diagnose_configuration_issue", "description": "Diagnose JDE configuration issues"},
    {"name": "lookup_esu_asu_requirements", "description": "Get ESU/ASU requirements"},
    {"name": "get_weblogic_configuration", "description": "Get WebLogic configuration"},
    {"name": "get_configuration_utilities_guide", "description": "Get P01RS01 Configuration Utilities guide"},
    {"name": "search_jde_documentation", "description": "Search JDE documentation"},
    {"name": "get_log_analysis_guidance", "description": "Get log analysis guidance"},
    {"name": "configure_multi_environment", "description": "Multi-environment setup guidance"},
]

RESOURCES = [
    {"uri": "jde://config/installation-checklist", "name": "Installation Checklist"},
    {"uri": "jde://config/environment-templates/production", "name": "Production Template (PD920)"},
    {"uri": "jde://config/environment-templates/test", "name": "Test Template (PY920)"},
    {"uri": "jde://config/environment-templates/development", "name": "Development Template (DV920)"},
    {"uri": "jde://reference/port-assignments", "name": "Port Assignments"},
    {"uri": "jde://reference/tools-release-matrix", "name": "Tools Release Matrix"},
    {"uri": "jde://reference/error-codes", "name": "Error Codes Reference"},
]

PROMPTS = [
    {"name": "new-environment-setup", "description": "New environment setup workflow"},
    {"name": "troubleshoot-deployment", "description": "Deployment troubleshooting"},
    {"name": "upgrade-planning", "description": "Tools Release upgrade planning"},
    {"name": "security-configuration", "description": "Security configuration guidance"},
]


async def health_check(request: web.Request) -> web.Response:
    """Health check endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "jde-e1-config-mcp",
        "version": "1.0.0"
    })


async def index_handler(request: web.Request) -> web.Response:
    """Root endpoint with API documentation."""
    return web.json_response({
        "name": "JDE E1 9.2 R24 Configuration Research MCP",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /": "API documentation",
            "GET /health": "Health check",
            "GET /tools": "List tools",
            "GET /resources": "List resources",
            "GET /prompts": "List prompts",
            "POST /tools/call": "Call a tool",
        },
        "tools_count": len(TOOLS),
        "resources_count": len(RESOURCES),
        "prompts_count": len(PROMPTS)
    })


async def list_tools(request: web.Request) -> web.Response:
    """List available tools."""
    return web.json_response({"tools": TOOLS})


async def list_resources(request: web.Request) -> web.Response:
    """List available resources."""
    return web.json_response({"resources": RESOURCES})


async def list_prompts(request: web.Request) -> web.Response:
    """List available prompts."""
    return web.json_response({"prompts": PROMPTS})


async def call_tool(request: web.Request) -> web.Response:
    """Call a tool and return results."""
    try:
        data = await request.json()
        tool_name = data.get("name", "")
        arguments = data.get("arguments", {})
        
        result = execute_tool(tool_name, arguments)
        return web.json_response({"result": result})
    except Exception as e:
        logger.error(f"Error calling tool: {e}")
        return web.json_response({"error": str(e)}, status=500)


def execute_tool(name: str, arguments: dict) -> dict:
    """Execute a tool and return the result."""
    
    if name == "research_installation_prerequisites":
        component = arguments.get("component", "all")
        platform = arguments.get("platform", "windows")
        if component == "all":
            return {"platform": platform, "prerequisites": INSTALLATION_PREREQUISITES}
        prereq = INSTALLATION_PREREQUISITES.get(component, {})
        return {"component": component, "platform": platform, "prerequisites": prereq.get(platform, prereq)}
    
    elif name == "get_installation_sequence":
        env_type = arguments.get("environment_type", "production")
        return {"environment_type": env_type, "sequence": INSTALLATION_SEQUENCE.get(env_type, [])}
    
    elif name == "get_environment_configuration":
        environment = arguments.get("environment", "PD920_production")
        return {"environment": environment, "configuration": ENVIRONMENT_CONFIG.get(environment, {})}
    
    elif name == "research_server_manager_config":
        config_area = arguments.get("config_area", "deployment_server")
        return {"config_area": config_area, "configuration": SERVER_MANAGER_CONFIG.get(config_area, {})}
    
    elif name == "get_centralized_configuration_guide":
        scope = arguments.get("scope", "overview")
        return {"scope": scope, "guide": CENTRALIZED_CONFIGURATION.get(scope, {})}
    
    elif name == "diagnose_configuration_issue":
        component = arguments.get("component", "")
        symptom = arguments.get("symptom", "")
        issues = TROUBLESHOOTING_GUIDE.get(component, {}).get("common_issues", [])
        return {"component": component, "symptom": symptom, "related_issues": issues}
    
    elif name == "lookup_esu_asu_requirements":
        feature = arguments.get("feature_area", "general")
        return {"feature_area": feature, "requirements": ESU_ASU_REQUIREMENTS.get(feature, {})}
    
    elif name == "get_weblogic_configuration":
        return {"weblogic": SERVER_MANAGER_CONFIG.get("html_server", {})}
    
    elif name == "get_configuration_utilities_guide":
        area = arguments.get("utility_area", "overview")
        return {"utility_area": area, "guide": CONFIGURATION_UTILITIES.get(area, {})}
    
    elif name == "get_log_analysis_guidance":
        log_type = arguments.get("log_type", "all")
        if log_type == "all":
            return {"log_analysis": LOG_ANALYSIS}
        return {"log_type": log_type, "analysis": LOG_ANALYSIS.get(log_type, {})}
    
    elif name == "search_jde_documentation":
        topic = arguments.get("topic", "")
        return {
            "topic": topic,
            "resources": [
                {"name": "Oracle JDE Documentation", "url": "https://docs.oracle.com/en/applications/jd-edwards/"},
                {"name": "My Oracle Support", "url": "https://support.oracle.com"}
            ]
        }
    
    elif name == "configure_multi_environment":
        model = arguments.get("deployment_model", "distributed")
        envs = arguments.get("environments", [])
        return {
            "deployment_model": model,
            "environments": envs,
            "guidance": {
                "single_server": "All environments on one server - use port offsets",
                "distributed": "Recommended - separate servers per environment",
                "cloud_hybrid": "Mix of on-prem and cloud deployment"
            }.get(model, "")
        }
    
    return {"error": f"Unknown tool: {name}"}


def create_app() -> web.Application:
    """Create the aiohttp application."""
    app = web.Application()
    app.router.add_get("/", index_handler)
    app.router.add_get("/health", health_check)
    app.router.add_get("/tools", list_tools)
    app.router.add_get("/resources", list_resources)
    app.router.add_get("/prompts", list_prompts)
    app.router.add_post("/tools/call", call_tool)
    return app


def main():
    """Run the HTTP server."""
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting JDE E1 MCP HTTP Server on port {port}")
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
