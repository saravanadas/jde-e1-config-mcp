"""
JDE E1 9.2 R24 Troubleshooting Guide
Contains troubleshooting data, log analysis, and configuration utilities info.
"""

# ============================================================================
# TROUBLESHOOTING GUIDE
# ============================================================================

TROUBLESHOOTING_GUIDE = {
    "deployment_server": {
        "common_issues": [
            {
                "symptom": "Package build fails",
                "error_messages": [
                    "Package build terminated with errors",
                    "Object check-out conflict",
                    "Insufficient disk space"
                ],
                "causes": [
                    "Insufficient disk space on deployment server",
                    "Object check-out conflicts in OMW",
                    "Database connectivity issues",
                    "Missing specifications"
                ],
                "diagnostic_steps": [
                    "Check disk space: dir /s on package build directory",
                    "Review Package Build log in Server Manager",
                    "Check OMW for conflicting check-outs",
                    "Verify database connectivity"
                ],
                "resolution": [
                    "Free up disk space or add storage",
                    "Resolve OMW check-out conflicts",
                    "Verify database connection settings",
                    "Rebuild specifications if needed"
                ],
                "log_files": [
                    "Server Manager Package Build Log",
                    "JDE.LOG on Deployment Server"
                ]
            },
            {
                "symptom": "Server Manager won't start",
                "error_messages": [
                    "Cannot connect to database",
                    "Port already in use",
                    "Service failed to start"
                ],
                "causes": [
                    "Database connection failure",
                    "Port conflicts with other applications",
                    "Service account credential issues",
                    "Corrupted configuration"
                ],
                "diagnostic_steps": [
                    "Check Windows Event Log for service errors",
                    "Verify database connectivity via ODBC",
                    "Check port availability: netstat -an | find \"7001\"",
                    "Validate service account credentials"
                ],
                "resolution": [
                    "Verify and fix database connection",
                    "Change ports or stop conflicting service",
                    "Reset service account password",
                    "Reinstall Server Manager if configuration corrupted"
                ],
                "log_files": [
                    "Windows Event Log > Application",
                    "Server Manager logs in install directory"
                ]
            },
            {
                "symptom": "ESU/ASU deployment fails",
                "causes": [
                    "Missing prerequisites",
                    "Incorrect deployment sequence",
                    "Database errors"
                ],
                "resolution": [
                    "Verify all prerequisites are met",
                    "Follow deployment sequence in special instructions",
                    "Check database for errors",
                    "Review ESU/ASU deployment log"
                ]
            }
        ]
    },
    "html_server": {
        "common_issues": [
            {
                "symptom": "Cannot access web client",
                "error_messages": [
                    "Connection refused",
                    "404 Not Found",
                    "503 Service Unavailable"
                ],
                "causes": [
                    "WebLogic server not running",
                    "Port blocked by firewall",
                    "SSL certificate issues",
                    "JAS application not deployed"
                ],
                "diagnostic_steps": [
                    "Check WebLogic Admin Console status",
                    "Verify managed server is running",
                    "Test port connectivity: telnet server 7003",
                    "Check firewall rules"
                ],
                "resolution": [
                    "Start WebLogic admin and managed servers",
                    "Open required ports in firewall",
                    "Renew or fix SSL certificates",
                    "Redeploy JAS application"
                ],
                "log_files": [
                    "WebLogic Server Log: $DOMAIN_HOME/servers/*/logs/*.log",
                    "JAS Log: $DOMAIN_HOME/servers/*/logs/jas*.log"
                ]
            },
            {
                "symptom": "Slow web client performance",
                "causes": [
                    "Insufficient JVM heap memory",
                    "Network latency",
                    "Database query performance",
                    "Too many concurrent users"
                ],
                "resolution": [
                    "Increase JVM heap settings (-Xmx)",
                    "Optimize network configuration",
                    "Review and optimize slow queries",
                    "Scale out with additional managed servers"
                ]
            },
            {
                "symptom": "Session timeout issues",
                "causes": [
                    "Incorrect timeout configuration",
                    "Load balancer timeout mismatch"
                ],
                "resolution": [
                    "Adjust session timeout in jas.ini",
                    "Align load balancer timeout settings",
                    "Configure sticky sessions if using load balancer"
                ]
            }
        ]
    },
    "enterprise_server": {
        "common_issues": [
            {
                "symptom": "Batch jobs not running",
                "causes": [
                    "Batch queue not started",
                    "Job scheduler issue",
                    "Database connectivity"
                ],
                "diagnostic_steps": [
                    "Check batch queue status in Server Manager",
                    "Review job scheduler configuration",
                    "Verify Enterprise Server kernels are running"
                ],
                "resolution": [
                    "Start batch queue via Server Manager",
                    "Restart job scheduler",
                    "Verify database connectivity",
                    "Check UBE logs for specific errors"
                ],
                "log_files": [
                    "JDE.LOG on Enterprise Server",
                    "UBE output files in PrintQueue directory"
                ]
            },
            {
                "symptom": "JDENET kernel crashes",
                "causes": [
                    "Memory exhaustion",
                    "Too many connections",
                    "Network issues"
                ],
                "resolution": [
                    "Increase kernel memory allocation",
                    "Optimize connection pooling",
                    "Review network configuration"
                ]
            }
        ]
    },
    "database": {
        "common_issues": [
            {
                "symptom": "Database connection timeouts",
                "causes": [
                    "Network issues",
                    "Database overloaded",
                    "Connection pool exhausted"
                ],
                "resolution": [
                    "Check network connectivity",
                    "Review database performance",
                    "Increase connection pool size"
                ]
            },
            {
                "symptom": "Table conversion errors",
                "causes": [
                    "Missing indexes",
                    "Data integrity issues",
                    "Insufficient space"
                ],
                "resolution": [
                    "Rebuild missing indexes",
                    "Clean up data integrity issues",
                    "Add database storage"
                ]
            }
        ]
    }
}

# ============================================================================
# LOG ANALYSIS GUIDANCE
# ============================================================================

LOG_ANALYSIS = {
    "jde_log": {
        "location": {
            "windows": "C:\\JDEdwards\\E920\\system\\bin32\\jde.log",
            "linux": "/u01/jdedwards/e920/system/bin32/jde.log"
        },
        "description": "Main JDE application log",
        "key_patterns": [
            {
                "pattern": "Error",
                "meaning": "General error condition",
                "action": "Review error details and context"
            },
            {
                "pattern": "BSFN ERROR",
                "meaning": "Business function error",
                "action": "Check BSFN name and error code"
            },
            {
                "pattern": "SQL Error",
                "meaning": "Database query error",
                "action": "Review SQL statement and database logs"
            }
        ]
    },
    "jas_log": {
        "location": "$DOMAIN_HOME/servers/*/logs/jas*.log",
        "description": "JDE Application Server log for web client",
        "key_patterns": [
            {
                "pattern": "Exception",
                "meaning": "Java exception occurred",
                "action": "Review full stack trace"
            },
            {
                "pattern": "OutOfMemoryError",
                "meaning": "JVM heap exhausted",
                "action": "Increase heap size or investigate memory leak"
            }
        ]
    },
    "weblogic_log": {
        "location": "$DOMAIN_HOME/servers/*/logs/*server.log",
        "description": "WebLogic server log",
        "key_patterns": [
            {
                "pattern": "BEA-",
                "meaning": "WebLogic-specific message",
                "action": "Look up BEA error code"
            },
            {
                "pattern": "Stuck Thread",
                "meaning": "Thread blocked for extended period",
                "action": "Review thread dump, check for deadlocks"
            }
        ]
    },
    "server_manager_log": {
        "location": "Server Manager installation directory/logs",
        "description": "Server Manager operation logs",
        "key_patterns": [
            {
                "pattern": "Deployment",
                "meaning": "Package deployment activity",
                "action": "Review deployment status"
            }
        ]
    },
    "package_build_log": {
        "location": "Server Manager > Package Build History",
        "description": "Package build detailed log",
        "key_patterns": [
            {
                "pattern": "BLDPKG ERROR",
                "meaning": "Package build error",
                "action": "Review error details, check object status"
            }
        ]
    }
}

# ============================================================================
# CONFIGURATION UTILITIES
# ============================================================================

CONFIGURATION_UTILITIES = {
    "overview": {
        "program": "P01RS01",
        "name": "JD Edwards EnterpriseOne Configuration Utilities",
        "description": "Central point for configuration programs and tools to set up and configure business data, task views, roles, security, and program versions",
        "menu": "GH9612",
        "capabilities": [
            "Import and export large amounts of data during initial setup",
            "Configure business processes across modules",
            "Set up valid configurations and implementations",
            "Manage roles and security settings",
            "Configure program versions"
        ]
    },
    "business_data": {
        "description": "Configure master data and business rules",
        "programs": [
            {
                "program": "P0004A",
                "name": "User Defined Codes",
                "purpose": "Maintain user defined code tables"
            },
            {
                "program": "P0006A",
                "name": "Business Unit Master",
                "purpose": "Configure business unit hierarchy"
            },
            {
                "program": "P0010",
                "name": "Company Setup",
                "purpose": "Configure company-level settings"
            }
        ]
    },
    "task_views": {
        "description": "Configure task views and navigation",
        "programs": [
            {
                "program": "P9000",
                "name": "Task View Configuration",
                "purpose": "Set up task views for different user roles"
            }
        ]
    },
    "roles": {
        "description": "Configure user roles and permissions",
        "programs": [
            {
                "program": "P00950",
                "name": "Role Master",
                "purpose": "Define and maintain user roles"
            },
            {
                "program": "P00951",
                "name": "Role Relationship",
                "purpose": "Configure role hierarchies and relationships"
            }
        ]
    },
    "security": {
        "description": "Configure security settings",
        "programs": [
            {
                "program": "P00950",
                "name": "User Security",
                "purpose": "Configure user-level security"
            },
            {
                "program": "P00105",
                "name": "Application Security",
                "purpose": "Configure application-level security"
            },
            {
                "program": "P00950W",
                "name": "Row Security",
                "purpose": "Configure row-level data security"
            }
        ]
    },
    "program_versions": {
        "description": "Configure program versions",
        "programs": [
            {
                "program": "P98305",
                "name": "Version Prompting Setup",
                "purpose": "Configure version selection behavior"
            },
            {
                "program": "P983051",
                "name": "Batch Version Configuration",
                "purpose": "Configure batch job versions"
            }
        ]
    }
}
