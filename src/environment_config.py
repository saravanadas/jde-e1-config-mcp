"""
JDE E1 9.2 R24 Environment Configuration
Contains environment-specific settings, server manager config, and centralized configuration.
"""

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

ENVIRONMENT_CONFIG = {
    "PD920_production": {
        "path_code": "PD920",
        "environment_name": "Production",
        "description": "Production Environment - Live business operations",
        "release": "9.2 R24",
        "data_sources": {
            "system": {
                "name": "System - PD920",
                "database": "JDE_SYSTEM_PD",
                "type": "System Tables",
                "tables": ["F0092", "F0093", "F0094", "F98101"]
            },
            "business_data": {
                "name": "Business Data - PD920",
                "database": "JDE_BUSDATA_PD",
                "type": "Business Data Tables",
                "tables": ["F0101", "F0411", "F4211", "F4311"]
            },
            "central_objects": {
                "name": "Central Objects - PD920",
                "database": "JDE_CENTRAL_PD",
                "type": "Central Objects",
                "tables": ["F9860", "F9861", "F9862"]
            },
            "versions": {
                "name": "Versions - PD920",
                "database": "JDE_VERSIONS_PD",
                "type": "Report Versions",
                "tables": ["F983051", "F98306"]
            },
            "control_tables": {
                "name": "Control Tables - PD920",
                "database": "JDE_CONTROL_PD",
                "type": "Control Tables",
                "tables": ["F0004", "F0005", "F0006", "F0010"]
            }
        },
        "server_map": {
            "enterprise_server": {
                "name": "ENT_PD920",
                "host": "jde-ent-prod.company.com",
                "port_range": "6000-6100"
            },
            "html_server": {
                "name": "HTML_PD920",
                "host": "jde-web-prod.company.com",
                "port": 7003,
                "url": "https://jde.company.com/jde"
            }
        },
        "ocm_mappings": {
            "description": "Object Configuration Manager mappings for production",
            "rules": [
                "All objects default to production data sources",
                "No development objects allowed in production OCM",
                "Custom objects must follow naming convention (55-59)"
            ]
        },
        "best_practices": [
            "Implement strict change control procedures - all changes via OMW projects",
            "Regular backups before any changes (daily differential, weekly full)",
            "Use Server Manager for all deployments - never manual file copies",
            "Monitor performance metrics continuously via Server Manager",
            "Implement row-level security for sensitive data",
            "Enable audit logging for compliance",
            "Schedule batch jobs during off-peak hours",
            "Maintain disaster recovery procedures"
        ],
        "security_level": "Highest",
        "change_control": "Required - All changes must be approved"
    },
    "PY920_test": {
        "path_code": "PY920",
        "environment_name": "Prototype/Test",
        "description": "Test/QA Environment - UAT and integration testing",
        "release": "9.2 R24",
        "data_sources": {
            "system": {
                "name": "System - PY920",
                "database": "JDE_SYSTEM_PY",
                "type": "System Tables"
            },
            "business_data": {
                "name": "Business Data - PY920",
                "database": "JDE_BUSDATA_PY",
                "type": "Business Data Tables"
            },
            "central_objects": {
                "name": "Central Objects - PY920",
                "database": "JDE_CENTRAL_PY",
                "type": "Central Objects"
            },
            "versions": {
                "name": "Versions - PY920",
                "database": "JDE_VERSIONS_PY",
                "type": "Report Versions"
            },
            "control_tables": {
                "name": "Control Tables - PY920",
                "database": "JDE_CONTROL_PY",
                "type": "Control Tables"
            }
        },
        "best_practices": [
            "Mirror production configuration where possible",
            "Use for UAT and integration testing before production",
            "Refresh data from production periodically (monthly recommended)",
            "Document all test scenarios and results",
            "Use realistic data volumes for performance testing",
            "Test all customizations thoroughly before promotion"
        ],
        "security_level": "Medium",
        "change_control": "Recommended"
    },
    "DV920_development": {
        "path_code": "DV920",
        "environment_name": "Development",
        "description": "Development Environment - Object development and unit testing",
        "release": "9.2 R24",
        "data_sources": {
            "system": {
                "name": "System - DV920",
                "database": "JDE_SYSTEM_DV",
                "type": "System Tables"
            },
            "business_data": {
                "name": "Business Data - DV920",
                "database": "JDE_BUSDATA_DV",
                "type": "Business Data Tables"
            },
            "central_objects": {
                "name": "Central Objects - DV920",
                "database": "JDE_CENTRAL_DV",
                "type": "Central Objects"
            },
            "versions": {
                "name": "Versions - DV920",
                "database": "JDE_VERSIONS_DV",
                "type": "Report Versions"
            },
            "control_tables": {
                "name": "Control Tables - DV920",
                "database": "JDE_CONTROL_DV",
                "type": "Control Tables"
            }
        },
        "development_tools": {
            "omw": {
                "name": "Object Management Workbench",
                "program": "P98220",
                "purpose": "Manage development projects and object lifecycle"
            },
            "oda": {
                "name": "Object Design Aid",
                "purpose": "Design and modify JDE objects"
            },
            "fda": {
                "name": "Form Design Aid",
                "purpose": "Create and modify interactive applications"
            },
            "rda": {
                "name": "Report Design Aid",
                "purpose": "Create and modify batch reports"
            }
        },
        "best_practices": [
            "Allow more flexibility for development activities",
            "Regular code promotions to test (weekly)",
            "Use Object Management Workbench (OMW) for all object changes",
            "Maintain development standards documentation",
            "Follow naming conventions for custom objects (55-59 prefix)",
            "Implement code review process before promotion",
            "Unit test all changes before moving to test environment"
        ],
        "security_level": "Lower",
        "change_control": "Optional - Developer discretion"
    }
}

# ============================================================================
# CENTRALIZED CONFIGURATION (Release 24 Feature)
# ============================================================================

CENTRALIZED_CONFIGURATION = {
    "overview": {
        "description": "Release 24 introduces Centralized Configuration to simplify management of settings across servers from Server Manager",
        "version_introduced": "Release 24 (9.2.7+)",
        "benefits": [
            "Set up default configuration that servers can inherit",
            "Reduces manual configuration effort across environments",
            "Ensures consistent settings across all managed servers",
            "Easier maintenance and updates - change once, apply everywhere",
            "Simplified onboarding of new servers",
            "Audit trail for configuration changes"
        ],
        "components": [
            "Server Manager Central Configuration",
            "Configuration Templates",
            "Inheritance Rules",
            "Override Management"
        ]
    },
    "setup": {
        "prerequisites": [
            "Server Manager 9.2.7 or higher",
            "Administrative access to Server Manager",
            "All managed servers registered in Server Manager"
        ],
        "steps": [
            {
                "step": 1,
                "action": "Access Server Manager",
                "details": "Log in to Server Manager with administrator credentials"
            },
            {
                "step": 2,
                "action": "Navigate to Centralized Configuration",
                "details": "Select 'Centralized Configuration' from the Configuration menu"
            },
            {
                "step": 3,
                "action": "Define Default Configuration Templates",
                "details": "Create templates for common configurations (Enterprise Server, HTML Server, etc.)"
            },
            {
                "step": 4,
                "action": "Assign Templates to Server Groups",
                "details": "Group servers by type or environment and assign appropriate templates"
            },
            {
                "step": 5,
                "action": "Configure Inheritance Rules",
                "details": "Define which settings can be overridden at server level"
            },
            {
                "step": 6,
                "action": "Test Configuration Deployment",
                "details": "Deploy configuration to test servers first, then production"
            }
        ]
    },
    "inheritance": {
        "description": "Inheritance allows servers to receive default settings while permitting local overrides",
        "hierarchy": [
            "Global Defaults -> Server Type Defaults -> Environment Defaults -> Individual Server",
        ],
        "override_behavior": [
            "Child settings override parent settings",
            "Locked settings cannot be overridden",
            "Audit log tracks all overrides"
        ]
    },
    "troubleshooting": {
        "common_issues": [
            {
                "issue": "Configuration not applying to server",
                "causes": ["Server not registered", "Template not assigned", "Inheritance blocked"],
                "resolution": "Verify server registration, check template assignment, review inheritance rules"
            },
            {
                "issue": "Unexpected configuration values",
                "causes": ["Override in effect", "Wrong template assigned", "Stale cache"],
                "resolution": "Check for local overrides, verify template assignment, refresh server configuration"
            }
        ]
    }
}

# ============================================================================
# SERVER MANAGER CONFIGURATION
# ============================================================================

SERVER_MANAGER_CONFIG = {
    "deployment_server": {
        "initial_setup": {
            "description": "Configure Deployment Server for JDE E1 9.2 R24",
            "steps": [
                {
                    "step": 1,
                    "action": "Install Server Manager",
                    "details": "Run Server Manager installer on Windows Server"
                },
                {
                    "step": 2,
                    "action": "Configure Database Connection",
                    "details": "Set up ODBC connection to JDE system database"
                },
                {
                    "step": 3,
                    "action": "Set Up Shared Directories",
                    "details": "Configure network shares for package deployment"
                },
                {
                    "step": 4,
                    "action": "Configure Deployment Locations",
                    "details": "Define paths for package builds and deployment"
                },
                {
                    "step": 5,
                    "action": "Register Managed Servers",
                    "details": "Add Enterprise and HTML servers to Server Manager"
                }
            ]
        },
        "package_deployment": {
            "description": "Deploy packages to target environments",
            "steps": [
                {
                    "step": 1,
                    "action": "Create Package Build",
                    "details": "Use Package Build to create deployment package"
                },
                {
                    "step": 2,
                    "action": "Select Target Environment",
                    "details": "Choose destination environment (DEV/TEST/PROD)"
                },
                {
                    "step": 3,
                    "action": "Deploy Package",
                    "details": "Execute deployment and monitor progress"
                },
                {
                    "step": 4,
                    "action": "Verify Deployment",
                    "details": "Check deployment status and logs"
                }
            ]
        }
    },
    "enterprise_server": {
        "initial_setup": {
            "description": "Configure Enterprise Server for JDE E1 9.2 R24",
            "steps": [
                {
                    "step": 1,
                    "action": "Install Enterprise Server Components",
                    "details": "Use Server Manager to install Enterprise Server"
                },
                {
                    "step": 2,
                    "action": "Configure Host Code",
                    "details": "Set up host code for server identification"
                },
                {
                    "step": 3,
                    "action": "Configure Kernel Processes",
                    "details": "Set up JDENET, JDEQUEUE, and JDEIPC kernels"
                },
                {
                    "step": 4,
                    "action": "Configure Batch Processing",
                    "details": "Set up batch queues and job scheduling"
                },
                {
                    "step": 5,
                    "action": "Start Enterprise Server",
                    "details": "Start all kernel processes and verify status"
                }
            ]
        },
        "kernel_configuration": {
            "JDENET": {
                "description": "Network kernel for JDE communications",
                "settings": {
                    "max_connections": 100,
                    "timeout": 300,
                    "port_range": "6000-6100"
                }
            },
            "JDEQUEUE": {
                "description": "Queue kernel for asynchronous processing",
                "settings": {
                    "max_workers": 10,
                    "queue_size": 1000
                }
            },
            "JDEIPC": {
                "description": "IPC kernel for inter-process communication",
                "settings": {
                    "shared_memory_size": "512MB"
                }
            }
        }
    },
    "html_server": {
        "initial_setup": {
            "description": "Configure HTML Server (Web Client) for JDE E1 9.2 R24",
            "steps": [
                {
                    "step": 1,
                    "action": "Install WebLogic Server Prerequisites",
                    "details": "Install JDK and configure JAVA_HOME"
                },
                {
                    "step": 2,
                    "action": "Deploy HTML Server via Server Manager",
                    "details": "Use Server Manager to deploy JAS instance"
                },
                {
                    "step": 3,
                    "action": "Configure WebLogic Domain",
                    "details": "Create JDE HTML domain with managed servers"
                },
                {
                    "step": 4,
                    "action": "Configure Managed Servers",
                    "details": "Set up managed server instances for each environment"
                },
                {
                    "step": 5,
                    "action": "Set Up AIS Services",
                    "details": "Configure Application Interface Services if required"
                },
                {
                    "step": 6,
                    "action": "Configure SSL (Optional)",
                    "details": "Set up SSL certificates for HTTPS access"
                },
                {
                    "step": 7,
                    "action": "Start HTML Server",
                    "details": "Start WebLogic admin and managed servers"
                }
            ]
        },
        "ports": {
            "admin_server": {
                "default": 7001,
                "description": "WebLogic Administration Server"
            },
            "managed_server": {
                "default": 7003,
                "description": "JDE HTML Managed Server"
            },
            "ais_server": {
                "default": 7075,
                "description": "Application Interface Services"
            }
        },
        "jvm_settings": {
            "initial_heap": "-Xms4096m",
            "max_heap": "-Xmx8192m",
            "metaspace": "-XX:MetaspaceSize=512m",
            "gc_options": "-XX:+UseG1GC"
        }
    }
}

# ============================================================================
# ESU/ASU REQUIREMENTS
# ============================================================================

ESU_ASU_REQUIREMENTS = {
    "orchestrator": {
        "description": "JDE Orchestrator for workflow automation",
        "required_components": [
            {
                "type": "ESU",
                "name": "Orchestrator Foundation",
                "mos_reference": "Check MOS for current Bug number",
                "notes": "Required for basic Orchestrator functionality"
            },
            {
                "type": "ASU",
                "name": "Orchestrator Studio",
                "version": "TL92500102+",
                "notes": "Design-time component for creating orchestrations"
            }
        ],
        "prerequisites": [
            "AIS Server configured and running",
            "HTML Server with REST services enabled"
        ]
    },
    "ux_one": {
        "description": "UX One role-based user experience",
        "required_components": [
            {
                "type": "ASU",
                "name": "UX One Foundation",
                "notes": "Base components for UX One"
            },
            {
                "type": "Content",
                "name": "UX One Role Content",
                "notes": "Role-specific content packages"
            }
        ]
    },
    "cafe_one": {
        "description": "CafeOne landing pages and dashboards",
        "required_components": [
            {
                "type": "ASU",
                "name": "CafeOne Framework",
                "notes": "Landing page framework"
            }
        ]
    },
    "e1_page": {
        "description": "E1 Page Composer for custom pages",
        "required_components": [
            {
                "type": "Tools",
                "name": "E1 Page Composer Tools",
                "notes": "Design tools for creating custom pages"
            }
        ]
    },
    "mobile": {
        "description": "JDE Mobile Enterprise applications",
        "required_components": [
            {
                "type": "ESU",
                "name": "Mobile Foundation",
                "notes": "Required for mobile app connectivity"
            },
            {
                "type": "Content",
                "name": "Mobile Application Content",
                "notes": "Pre-built mobile applications"
            }
        ],
        "prerequisites": [
            "AIS Server with mobile services enabled",
            "SSL certificate for secure mobile connections"
        ]
    }
}
