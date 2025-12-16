# JDE E1 9.2 R24 System Configuration Research MCP

[![MCP](https://img.shields.io/badge/MCP-1.0.0-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

An MCP (Model Context Protocol) server that provides comprehensive research and guidance tools for **JD Edwards EnterpriseOne 9.2 Release 24** system configuration. Designed for deployment on [SimTheory.ai](https://simtheory.ai).

## Overview

This MCP server enables AI-assisted research and configuration guidance for JDE E1 administrators, consultants, and developers. It provides structured access to installation procedures, environment configuration, troubleshooting guidance, and best practices.

## Features

### 🔧 Tools (12 Available)

| Tool | Description |
|------|-------------|
| `research_installation_prerequisites` | Get prerequisites for JDE components (Deployment Server, Enterprise Server, HTML Server, Database) |
| `get_installation_sequence` | Detailed installation steps with durations and checkpoints |
| `get_environment_configuration` | Configuration for PD920 (Production), PY920 (Test), DV920 (Development) |
| `research_server_manager_config` | Server Manager setup and configuration guidance |
| `get_centralized_configuration_guide` | Release 24's new Centralized Configuration feature |
| `diagnose_configuration_issue` | Troubleshooting with symptoms, causes, and resolutions |
| `lookup_esu_asu_requirements` | ESU/ASU requirements for Orchestrator, UX One, Mobile, etc. |
| `get_weblogic_configuration` | WebLogic Server configuration for HTML/AIS servers |
| `get_configuration_utilities_guide` | P01RS01 Configuration Utilities guidance |
| `search_jde_documentation` | Search Oracle JDE documentation |
| `get_log_analysis_guidance` | Log file analysis with patterns and locations |
| `configure_multi_environment` | Multi-environment setup (PROD/TEST/DEV) |

### 📁 Resources (7 Available)

- `jde://config/installation-checklist` - Complete installation checklist
- `jde://config/environment-templates/production` - PD920 configuration template
- `jde://config/environment-templates/test` - PY920 configuration template
- `jde://config/environment-templates/development` - DV920 configuration template
- `jde://reference/port-assignments` - Standard JDE port assignments
- `jde://reference/tools-release-matrix` - Tools Release compatibility matrix
- `jde://reference/error-codes` - Common JDE error codes

### 💬 Prompts (4 Available)

- `new-environment-setup` - Guided workflow for new environment setup
- `troubleshoot-deployment` - Package deployment troubleshooting
- `upgrade-planning` - Tools Release upgrade planning
- `security-configuration` - Security configuration guidance

## Supported Environments

| Environment | Path Code | Description |
|-------------|-----------|-------------|
| Production | PD920 | Live business operations |
| Test/QA | PY920 | UAT and integration testing |
| Development | DV920 | Object development and unit testing |

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/saravanadas/jde-e1-config-mcp.git
cd jde-e1-config-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Install with uv

```bash
uv pip install -e .
```

## Usage

### Run the MCP Server

```bash
# Using Python
python -m src.server

# Or using the installed script
jde-e1-config-mcp
```

### Configure for Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "jde-e1-config": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/jde-e1-config-mcp"
    }
  }
}
```

### Deploy to SimTheory.ai

1. Navigate to SimTheory.ai MCP deployment
2. Upload the repository or connect via GitHub
3. Configure environment variables if needed
4. Deploy and test

## Example Tool Calls

### Get Installation Prerequisites

```json
{
  "name": "research_installation_prerequisites",
  "arguments": {
    "component": "html_server",
    "platform": "windows"
  }
}
```

### Diagnose Configuration Issue

```json
{
  "name": "diagnose_configuration_issue",
  "arguments": {
    "symptom": "Cannot access web client",
    "component": "html_server",
    "environment": "PD920"
  }
}
```

### Get Environment Configuration

```json
{
  "name": "get_environment_configuration",
  "arguments": {
    "environment": "PD920_production",
    "component": "data_sources"
  }
}
```

## Project Structure

```
jde-e1-config-mcp/
├── src/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── tests/
│   └── test_server.py     # Unit tests
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── LICENSE               # MIT License
└── README.md             # This file
```

## Knowledge Base Coverage

The MCP includes an embedded knowledge base covering:

- **Installation Prerequisites**: OS, runtime, middleware, hardware requirements
- **Installation Sequence**: Step-by-step procedures with durations
- **Environment Configuration**: Data sources, server maps, OCM mappings
- **Server Manager**: Deployment Server, Enterprise Server, HTML Server setup
- **Centralized Configuration**: Release 24 feature documentation
- **Troubleshooting**: Common issues, diagnostic steps, resolutions
- **ESU/ASU Requirements**: Patch requirements for various features
- **Log Analysis**: Log locations, key patterns, analysis techniques

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## References

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [Oracle JDE Documentation](https://docs.oracle.com/en/applications/jd-edwards/)
- [My Oracle Support](https://support.oracle.com)
- [Oracle Certifications](https://certification.oracle.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This MCP server provides guidance and research assistance. Always verify information against official Oracle documentation and consult Oracle Support for production implementations. This is not an official Oracle product.

## Author

Das Sivadas - [GitHub](https://github.com/saravanadas)

---

Built for [SimTheory.ai](https://simtheory.ai) | Powered by [MCP](https://modelcontextprotocol.io)
