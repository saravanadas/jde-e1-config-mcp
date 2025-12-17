#!/usr/bin/env python3
"""
JDE E1 9.2 R24 System Configuration Research MCP Server
Main server implementation with all tools, resources, and prompts.
For deployment on SimTheory.ai
"""

import asyncio
import json
import logging
from typing import Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    Prompt,
    PromptArgument,
    GetPromptResult,
    PromptMessage,
)

# Import knowledge base modules
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jde-e1-config-mcp")

# Initialize the MCP server
server = Server("jde-e1-config-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available JDE configuration research tools."""
    return [
        Tool(
            name="research_installation_prerequisites",
            description="Research and return the mandatory installation prerequisites for JDE E1 9.2 R24 components",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "enum": ["deployment_server", "enterprise_server", "html_server", "database", "all"],
                        "description": "The JDE component to get prerequisites for"
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["windows", "linux", "aix"],
                        "description": "Target platform",
                        "default": "windows"
                    }
                },
                "required": ["component"]
            }
        ),
        Tool(
            name="get_installation_sequence",
            description="Returns the mandatory installation sequence for JDE E1 9.2 R24 components",
            inputSchema={
                "type": "object",
                "properties": {
                    "environment_type": {
                        "type": "string",
                        "enum": ["production", "test_py", "development", "standalone_demo"],
                        "description": "Type of environment being installed"
                    }
                },
                "required": ["environment_type"]
            }
        ),
        Tool(
            name="get_environment_configuration",
            description="Provides configuration guidance for specific JDE environment types (PD920, PY920, DV920)",
            inputSchema={
                "type": "object",
                "properties": {
                    "environment": {
                        "type": "string",
                        "enum": ["PD920_production", "PY920_test", "DV920_development"],
                        "description": "The target environment"
                    },
                    "component": {
                        "type": "string",
                        "enum": ["path_codes", "data_sources", "ocm_mappings", "server_map", "all"],
                        "description": "Configuration component to retrieve",
                        "default": "all"
                    }
                },
                "required": ["environment"]
            }
        ),
        Tool(
            name="research_server_manager_config",
            description="Research Server Manager configuration options for JDE E1 9.2 R24",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_area": {
                        "type": "string",
                        "enum": ["deployment_server", "enterprise_server", "html_server", "batch_server", "logic_server"],
                        "description": "Server Manager configuration area"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["initial_setup", "add_environment", "package_deployment", "esus_asus", "kernel_configuration"],
                        "description": "Type of operation",
                        "default": "initial_setup"
                    }
                },
                "required": ["config_area"]
            }
        ),
        Tool(
            name="get_centralized_configuration_guide",
            description="Returns guidance on Release 24's new Centralized Configuration feature",
            inputSchema={
                "type": "object",
                "properties": {
                    "scope": {
                        "type": "string",
                        "enum": ["overview", "setup", "inheritance", "troubleshooting"],
                        "description": "Aspect of Centralized Configuration"
                    }
                },
                "required": ["scope"]
            }
        ),
        Tool(
            name="diagnose_configuration_issue",
            description="Diagnose common JDE E1 9.2 R24 configuration issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "symptom": {
                        "type": "string",
                        "description": "Description of the issue or symptom"
                    },
                    "component": {
                        "type": "string",
                        "enum": ["deployment_server", "enterprise_server", "html_server", "database", "client"],
                        "description": "Affected component"
                    },
                    "environment": {
                        "type": "string",
                        "description": "Environment where issue occurs (optional)"
                    }
                },
                "required": ["symptom", "component"]
            }
        ),
        Tool(
            name="lookup_esu_asu_requirements",
            description="Research required ESUs and ASUs for specific JDE E1 9.2 R24 features",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature_area": {
                        "type": "string",
                        "enum": ["orchestrator", "ux_one", "cafe_one", "e1_page", "mobile", "general"],
                        "description": "Feature area requiring ESU/ASU information"
                    },
                    "tools_release": {
                        "type": "string",
                        "description": "Tools release version",
                        "default": "9.2.7"
                    }
                },
                "required": ["feature_area"]
            }
        ),
        Tool(
            name="get_weblogic_configuration",
            description="Returns WebLogic Server configuration for JDE HTML/AIS servers",
            inputSchema={
                "type": "object",
                "properties": {
                    "server_type": {
                        "type": "string",
                        "enum": ["html_server", "ais_server", "admin_server"],
                        "description": "Type of WebLogic server"
                    },
                    "config_area": {
                        "type": "string",
                        "enum": ["initial_setup", "managed_servers", "clustering", "ssl", "ports", "jvm_settings"],
                        "description": "Configuration area",
                        "default": "initial_setup"
                    }
                },
                "required": ["server_type"]
            }
        ),
        Tool(
            name="get_configuration_utilities_guide",
            description="Returns guidance on using JDE Configuration Utilities (P01RS01)",
            inputSchema={
                "type": "object",
                "properties": {
                    "utility_area": {
                        "type": "string",
                        "enum": ["business_data", "task_views", "roles", "security", "program_versions", "overview"],
                        "description": "Configuration Utilities area"
                    }
                },
                "required": ["utility_area"]
            }
        ),
        Tool(
            name="search_jde_documentation",
            description="Search and summarize relevant Oracle JDE E1 9.2 R24 documentation",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search for"
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": ["installation_guide", "admin_guide", "security_guide", "upgrade_guide", "release_notes", "all"],
                        "description": "Type of documentation",
                        "default": "all"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="get_log_analysis_guidance",
            description="Returns guidance on analyzing JDE log files",
            inputSchema={
                "type": "object",
                "properties": {
                    "log_type": {
                        "type": "string",
                        "enum": ["jde_log", "jas_log", "weblogic_log", "server_manager_log", "package_build_log", "all"],
                        "description": "Type of log file to analyze"
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Specific issue type (optional)"
                    }
                },
                "required": ["log_type"]
            }
        ),
        Tool(
            name="configure_multi_environment",
            description="Guidance for multi-environment setup (PROD/TEST/DEV)",
            inputSchema={
                "type": "object",
                "properties": {
                    "deployment_model": {
                        "type": "string",
                        "enum": ["single_server", "distributed", "cloud_hybrid"],
                        "description": "Deployment model"
                    },
                    "environments": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of environments"
                    }
                },
                "required": ["deployment_model", "environments"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for JDE configuration research."""
    logger.info(f"Tool called: {name}")
    
    try:
        if name == "research_installation_prerequisites":
            component = arguments.get("component", "all")
            platform = arguments.get("platform", "windows")
            
            if component == "all":
                result = {"platform": platform, "prerequisites": {}}
                for comp in ["deployment_server", "enterprise_server", "html_server", "database"]:
                    prereq = INSTALLATION_PREREQUISITES.get(comp, {})
                    if platform in prereq:
                        result["prerequisites"][comp] = prereq[platform]
                    elif comp == "database":
                        result["prerequisites"][comp] = prereq
            else:
                prereq_data = INSTALLATION_PREREQUISITES.get(component, {})
                prereq = prereq_data.get(platform, prereq_data)
                result = {"component": component, "platform": platform, "prerequisites": prereq}
            
            result["notes"] = ["Verify against Oracle Certifications", "Check MOS for latest patches"]
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_installation_sequence":
            env_type = arguments.get("environment_type", "production")
            sequence = INSTALLATION_SEQUENCE.get(env_type, INSTALLATION_SEQUENCE["production"])
            result = {
                "environment_type": env_type,
                "installation_sequence": sequence,
                "notes": ["Follow steps in order", "Do not skip backups", "Document all changes"]
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_environment_configuration":
            environment = arguments.get("environment")
            component = arguments.get("component", "all")
            env_config = ENVIRONMENT_CONFIG.get(environment, {})
            
            if component == "all":
                result = {"environment": environment, "configuration": env_config}
            elif component == "data_sources":
                result = {"environment": environment, "data_sources": env_config.get("data_sources", {})}
            else:
                result = {"environment": environment, "component": component, "data": env_config.get(component, env_config)}
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "research_server_manager_config":
            config_area = arguments.get("config_area")
            operation = arguments.get("operation", "initial_setup")
            server_config = SERVER_MANAGER_CONFIG.get(config_area, {})
            
            if operation == "kernel_configuration" and config_area == "enterprise_server":
                config_data = server_config.get("kernel_configuration", {})
            else:
                config_data = server_config.get(operation, server_config.get("initial_setup", {}))
            
            result = {"config_area": config_area, "operation": operation, "configuration": config_data}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_centralized_configuration_guide":
            scope = arguments.get("scope", "overview")
            result = {
                "feature": "Centralized Configuration (Release 24)",
                "scope": scope,
                "details": CENTRALIZED_CONFIGURATION.get(scope, CENTRALIZED_CONFIGURATION["overview"])
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "diagnose_configuration_issue":
            symptom = arguments.get("symptom", "")
            component = arguments.get("component")
            environment = arguments.get("environment", "Not specified")
            
            component_issues = TROUBLESHOOTING_GUIDE.get(component, {}).get("common_issues", [])
            matching = [i for i in component_issues if any(w in symptom.lower() for w in i["symptom"].lower().split())]
            
            result = {
                "symptom": symptom,
                "component": component,
                "environment": environment,
                "matching_issues": matching if matching else "No exact match - use general troubleshooting",
                "general_steps": ["Check Server Manager logs", "Verify database connectivity", "Review JDE.LOG"]
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "lookup_esu_asu_requirements":
            feature_area = arguments.get("feature_area", "general")
            tools_release = arguments.get("tools_release", "9.2.7")
            feature_info = ESU_ASU_REQUIREMENTS.get(feature_area, {})
            
            result = {
                "feature_area": feature_area,
                "tools_release": tools_release,
                "requirements": feature_info,
                "note": "Check My Oracle Support for current patch numbers"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_weblogic_configuration":
            server_type = arguments.get("server_type")
            config_area = arguments.get("config_area", "initial_setup")
            html_config = SERVER_MANAGER_CONFIG.get("html_server", {})
            
            result = {
                "server_type": server_type,
                "config_area": config_area,
                "ports": html_config.get("ports", {}),
                "jvm_settings": html_config.get("jvm_settings", {}),
                "setup_steps": html_config.get("initial_setup", {}).get("steps", [])
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_configuration_utilities_guide":
            utility_area = arguments.get("utility_area", "overview")
            utility_info = CONFIGURATION_UTILITIES.get(utility_area, CONFIGURATION_UTILITIES["overview"])
            
            result = {
                "program": "P01RS01",
                "utility_area": utility_area,
                "details": utility_info,
                "menu": "GH9612"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "search_jde_documentation":
            topic = arguments.get("topic", "")
            result = {
                "topic": topic,
                "resources": [
                    {"title": "JDE Documentation Library", "url": "https://docs.oracle.com/en/applications/jd-edwards/"},
                    {"title": "My Oracle Support", "url": "https://support.oracle.com"}
                ]
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_log_analysis_guidance":
            log_type = arguments.get("log_type", "all")
            log_info = LOG_ANALYSIS if log_type == "all" else {log_type: LOG_ANALYSIS.get(log_type, {})}
            
            result = {"log_type": log_type, "analysis": log_info}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "configure_multi_environment":
            deployment_model = arguments.get("deployment_model")
            environments = arguments.get("environments", [])
            
            model_guidance = {
                "single_server": {"description": "All environments on single server", "port_offsets": 10},
                "distributed": {"description": "Separate servers per environment", "recommended": True},
                "cloud_hybrid": {"description": "Mix of on-prem and cloud", "cloud_options": ["OCI", "AWS", "Azure"]}
            }
            
            result = {
                "deployment_model": deployment_model,
                "environments": environments,
                "guidance": model_guidance.get(deployment_model, {})
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2))]
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available JDE configuration resources."""
    return [
        Resource(uri="jde://config/installation-checklist", name="Installation Checklist", mimeType="application/json"),
        Resource(uri="jde://config/environment-templates/production", name="Production Template (PD920)", mimeType="application/json"),
        Resource(uri="jde://config/environment-templates/test", name="Test Template (PY920)", mimeType="application/json"),
        Resource(uri="jde://config/environment-templates/development", name="Development Template (DV920)", mimeType="application/json"),
        Resource(uri="jde://reference/port-assignments", name="Port Assignments", mimeType="application/json"),
        Resource(uri="jde://reference/tools-release-matrix", name="Tools Release Matrix", mimeType="application/json"),
        Resource(uri="jde://reference/error-codes", name="Error Codes Reference", mimeType="application/json"),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read JDE configuration resources."""
    if uri == "jde://config/installation-checklist":
        return json.dumps({"checklist": INSTALLATION_SEQUENCE["production"], "prerequisites": INSTALLATION_PREREQUISITES}, indent=2)
    elif uri == "jde://config/environment-templates/production":
        return json.dumps(ENVIRONMENT_CONFIG["PD920_production"], indent=2)
    elif uri == "jde://config/environment-templates/test":
        return json.dumps(ENVIRONMENT_CONFIG["PY920_test"], indent=2)
    elif uri == "jde://config/environment-templates/development":
        return json.dumps(ENVIRONMENT_CONFIG["DV920_development"], indent=2)
    elif uri == "jde://reference/port-assignments":
        return json.dumps({"weblogic_admin": 7001, "managed": 7003, "ais": 7075, "http": 80, "https": 443}, indent=2)
    elif uri == "jde://reference/tools-release-matrix":
        return json.dumps({"current": "9.2.7", "databases": ["Oracle 19c", "SQL Server 2019+"], "weblogic": ["12.2.1.4", "14.1.1"]}, indent=2)
    elif uri == "jde://reference/error-codes":
        return json.dumps({"security": {"0001": "Invalid credentials"}, "database": {"DB001": "Connection failed"}}, indent=2)
    return json.dumps({"error": f"Resource not found: {uri}"})


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available JDE configuration prompts."""
    return [
        Prompt(name="new-environment-setup", description="New environment setup workflow",
               arguments=[PromptArgument(name="environment_name", required=True), PromptArgument(name="environment_type", required=True), PromptArgument(name="database_platform", required=True)]),
        Prompt(name="troubleshoot-deployment", description="Deployment troubleshooting",
               arguments=[PromptArgument(name="package_name", required=True), PromptArgument(name="target_environment", required=True), PromptArgument(name="error_description", required=True)]),
        Prompt(name="upgrade-planning", description="Tools Release upgrade planning",
               arguments=[PromptArgument(name="current_tools_release", required=True), PromptArgument(name="target_tools_release", required=True)]),
        Prompt(name="security-configuration", description="Security configuration guidance",
               arguments=[PromptArgument(name="security_level", required=True), PromptArgument(name="environment", required=True)]),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: Optional[dict] = None) -> GetPromptResult:
    """Get JDE configuration prompts."""
    args = arguments or {}
    
    if name == "new-environment-setup":
        return GetPromptResult(
            description=f"Setup guide for {args.get('environment_name', 'NEW_ENV')}",
            messages=[PromptMessage(role="user", content=TextContent(type="text",
                text=f"Set up JDE E1 9.2 R24 environment: {args.get('environment_name')} ({args.get('environment_type')}) with {args.get('database_platform')}. Provide prerequisites, installation steps, and verification."))]
        )
    elif name == "troubleshoot-deployment":
        return GetPromptResult(
            description=f"Troubleshoot {args.get('package_name')}",
            messages=[PromptMessage(role="user", content=TextContent(type="text",
                text=f"Troubleshoot deployment of {args.get('package_name')} to {args.get('target_environment')}. Error: {args.get('error_description')}"))]
        )
    elif name == "upgrade-planning":
        return GetPromptResult(
            description=f"Upgrade from {args.get('current_tools_release')} to {args.get('target_tools_release')}",
            messages=[PromptMessage(role="user", content=TextContent(type="text",
                text=f"Plan upgrade from Tools {args.get('current_tools_release')} to {args.get('target_tools_release')}. Include ESUs/ASUs, sequence, and rollback plan."))]
        )
    elif name == "security-configuration":
        return GetPromptResult(
            description=f"Security for {args.get('environment')}",
            messages=[PromptMessage(role="user", content=TextContent(type="text",
                text=f"Configure {args.get('security_level')} security for {args.get('environment')}. Include authentication, authorization, and audit settings."))]
        )
    return GetPromptResult(description="Unknown", messages=[])


async def main():
    """Run the JDE E1 Configuration Research MCP server."""
    logger.info("Starting JDE E1 9.2 R24 Configuration Research MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
