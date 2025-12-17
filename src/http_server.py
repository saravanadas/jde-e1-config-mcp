#!/usr/bin/env python3
"""
Simple HTTP Server for JDE E1 MCP - Railway Deployment
With Bearer Token Authentication
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jde-e1-http")

# Bearer token from environment variable
API_TOKEN = os.environ.get("API_TOKEN", "")

# Track import status for debugging
IMPORT_STATUS = {
    "knowledge_base": False,
    "environment_config": False,
    "troubleshooting": False,
    "errors": []
}

# Initialize empty defaults
INSTALLATION_PREREQUISITES = {}
INSTALLATION_SEQUENCE = {}
ENVIRONMENT_CONFIG = {}
CENTRALIZED_CONFIGURATION = {}
SERVER_MANAGER_CONFIG = {}
ESU_ASU_REQUIREMENTS = {}
TROUBLESHOOTING_GUIDE = {}
LOG_ANALYSIS = {}
CONFIGURATION_UTILITIES = {}

# Import knowledge base data with detailed error tracking
try:
    from .knowledge_base import INSTALLATION_PREREQUISITES, INSTALLATION_SEQUENCE
    IMPORT_STATUS["knowledge_base"] = True
    logger.info(f"knowledge_base imported: PREREQUISITES={len(INSTALLATION_PREREQUISITES)} items, SEQUENCE={len(INSTALLATION_SEQUENCE)} items")
except Exception as e:
    error_msg = f"knowledge_base import failed: {type(e).__name__}: {e}"
    IMPORT_STATUS["errors"].append(error_msg)
    logger.error(error_msg)

try:
    from .environment_config import (
        ENVIRONMENT_CONFIG,
        CENTRALIZED_CONFIGURATION,
        SERVER_MANAGER_CONFIG,
        ESU_ASU_REQUIREMENTS,
    )
    IMPORT_STATUS["environment_config"] = True
    logger.info(f"environment_config imported: ENV_CONFIG={len(ENVIRONMENT_CONFIG)} items")
except Exception as e:
    error_msg = f"environment_config import failed: {type(e).__name__}: {e}"
    IMPORT_STATUS["errors"].append(error_msg)
    logger.error(error_msg)

try:
    from .troubleshooting import (
        TROUBLESHOOTING_GUIDE,
        LOG_ANALYSIS,
        CONFIGURATION_UTILITIES,
    )
    IMPORT_STATUS["troubleshooting"] = True
    logger.info(f"troubleshooting imported: GUIDE={len(TROUBLESHOOTING_GUIDE)} items")
except Exception as e:
    error_msg = f"troubleshooting import failed: {type(e).__name__}: {e}"
    IMPORT_STATUS["errors"].append(error_msg)
    logger.error(error_msg)

logger.info(f"Import status: {IMPORT_STATUS}")

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


def execute_tool(name, arguments):
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


class JDEHandler(BaseHTTPRequestHandler):
    """HTTP request handler for JDE MCP API."""
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _check_auth(self):
        """Check bearer token authentication."""
        # If no token is configured, allow all requests
        if not API_TOKEN:
            return True
        
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix
            return token == API_TOKEN
        return False
    
    def _send_unauthorized(self):
        """Send 401 Unauthorized response."""
        self._send_json({"error": "Unauthorized. Bearer token required."}, 401)
    
    def do_GET(self):
        # Health check doesn't require auth
        if self.path == "/health":
            self._send_json({"status": "healthy", "service": "jde-e1-config-mcp"})
            return
        
        # All other endpoints require auth
        if not self._check_auth():
            self._send_unauthorized()
            return
        
        if self.path == "/" or self.path == "":
            self._send_json({
                "name": "JDE E1 9.2 R24 Configuration Research MCP",
                "version": "1.0.0",
                "status": "running",
                "tools_count": len(TOOLS),
                "resources_count": len(RESOURCES),
                "prompts_count": len(PROMPTS)
            })
        elif self.path == "/tools":
            self._send_json({"tools": TOOLS})
        elif self.path == "/resources":
            self._send_json({"resources": RESOURCES})
        elif self.path == "/prompts":
            self._send_json({"prompts": PROMPTS})
        elif self.path == "/debug":
            # Debug endpoint to check import status
            self._send_json({
                "import_status": IMPORT_STATUS,
                "data_counts": {
                    "INSTALLATION_PREREQUISITES": len(INSTALLATION_PREREQUISITES),
                    "INSTALLATION_SEQUENCE": len(INSTALLATION_SEQUENCE),
                    "ENVIRONMENT_CONFIG": len(ENVIRONMENT_CONFIG),
                    "CENTRALIZED_CONFIGURATION": len(CENTRALIZED_CONFIGURATION),
                    "SERVER_MANAGER_CONFIG": len(SERVER_MANAGER_CONFIG),
                    "ESU_ASU_REQUIREMENTS": len(ESU_ASU_REQUIREMENTS),
                    "TROUBLESHOOTING_GUIDE": len(TROUBLESHOOTING_GUIDE),
                    "LOG_ANALYSIS": len(LOG_ANALYSIS),
                    "CONFIGURATION_UTILITIES": len(CONFIGURATION_UTILITIES),
                },
                "environment_config_keys": list(ENVIRONMENT_CONFIG.keys()) if ENVIRONMENT_CONFIG else [],
                "python_path": sys.path,
                "working_directory": os.getcwd()
            })
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        # Check auth for all POST requests
        if not self._check_auth():
            self._send_unauthorized()
            return
        
        if self.path == "/tools/call":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            try:
                data = json.loads(body)
                result = execute_tool(data.get("name", ""), data.get("arguments", {}))
                self._send_json({"result": result})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()


def main():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), JDEHandler)
    
    if API_TOKEN:
        logger.info(f"Bearer token authentication ENABLED")
    else:
        logger.info(f"Bearer token authentication DISABLED (no API_TOKEN set)")
    
    logger.info(f"Starting JDE E1 MCP HTTP Server on 0.0.0.0:{port}")
    logger.info(f"Import status: {IMPORT_STATUS}")
    print(f"Server running on port {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
