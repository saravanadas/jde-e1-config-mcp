"""
JDE E1 9.2 R24 Knowledge Base
Contains all configuration data, prerequisites, and reference information.
"""

# ============================================================================
# INSTALLATION PREREQUISITES
# ============================================================================

INSTALLATION_PREREQUISITES = {
    "deployment_server": {
        "windows": {
            "os": [
                "Windows Server 2016 (64-bit)",
                "Windows Server 2019 (64-bit)",
                "Windows Server 2022 (64-bit)"
            ],
            "runtime": [
                "Microsoft Visual C++ 2010 Runtime X86 Redistributables",
                "Microsoft Visual C++ 2012 Runtime X86 Redistributables",
                "Microsoft Visual C++ 2013 Runtime X86 Redistributables",
                "Microsoft .NET Framework 4.8"
            ],
            "disk_space": {
                "minimum": "50GB",
                "recommended": "100GB",
                "notes": "Additional space needed for package builds and logs"
            },
            "memory": {
                "minimum": "16GB",
                "recommended": "32GB"
            },
            "network": {
                "requirements": [
                    "Static IP address",
                    "DNS resolution to all JDE servers",
                    "Network access to database server",
                    "Firewall rules for JDE ports"
                ]
            },
            "user_requirements": [
                "Local Administrator rights",
                "Database user with DBA privileges",
                "Service account for JDE services"
            ],
            "notes": "Deployment Server handles initial setup, package builds, and ESU/ASU deployment"
        },
        "linux": {
            "os": [
                "Oracle Linux 7.x (64-bit)",
                "Oracle Linux 8.x (64-bit)",
                "Red Hat Enterprise Linux 7.x (64-bit)",
                "Red Hat Enterprise Linux 8.x (64-bit)"
            ],
            "packages": [
                "glibc.i686",
                "libstdc++.i686",
                "libaio",
                "unzip",
                "ksh"
            ],
            "disk_space": {
                "minimum": "50GB",
                "recommended": "100GB"
            },
            "memory": {
                "minimum": "16GB",
                "recommended": "32GB"
            },
            "notes": "Linux Deployment Server requires additional configuration for 32-bit compatibility"
        }
    },
    "enterprise_server": {
        "windows": {
            "os": [
                "Windows Server 2016 (64-bit)",
                "Windows Server 2019 (64-bit)",
                "Windows Server 2022 (64-bit)"
            ],
            "middleware": {
                "weblogic": {
                    "versions": ["12.2.1.4", "14.1.1"],
                    "notes": "Check Oracle Certifications for exact version requirements"
                },
                "tuxedo": {
                    "versions": ["12.2.2", "22.1"],
                    "notes": "Required for batch processing and business logic"
                }
            },
            "java": {
                "versions": ["JDK 8u301+", "JDK 11.0.11+"],
                "notes": "Use Oracle JDK or OpenJDK certified versions only"
            },
            "memory": {
                "minimum": "32GB",
                "recommended": "64GB",
                "production": "128GB for high-volume environments"
            },
            "cpu": {
                "minimum": "8 cores",
                "recommended": "16 cores"
            },
            "kernel_configuration": {
                "JDENET": "Network kernel for JDE communications",
                "JDEQUEUE": "Queue kernel for asynchronous processing",
                "JDEIPC": "IPC kernel for inter-process communication"
            },
            "notes": "Enterprise Server runs business logic, batch processing, and kernel services"
        }
    },
    "html_server": {
        "windows": {
            "middleware": {
                "weblogic": {
                    "versions": ["12.2.1.4", "14.1.1"],
                    "domain_type": "JDE HTML Domain"
                },
                "oracle_http_server": {
                    "versions": ["12.2.1.4"],
                    "notes": "Optional - for load balancing and SSL termination"
                }
            },
            "java": {
                "versions": ["JDK 8u301+", "JDK 11.0.11+"]
            },
            "ports": {
                "admin_server": 7001,
                "managed_server": 7003,
                "ais_server": 7075,
                "http": 80,
                "https": 443,
                "notes": "Ports must be unique if running multiple environments on same server"
            },
            "memory": {
                "minimum": "16GB",
                "recommended": "32GB",
                "heap_settings": "-Xms4096m -Xmx8192m"
            },
            "notes": "HTML Server provides web interface, AIS services, and Orchestrator runtime"
        }
    },
    "database": {
        "sql_server": {
            "versions": [
                "SQL Server 2016 SP3",
                "SQL Server 2019",
                "SQL Server 2022"
            ],
            "collation": "SQL_Latin1_General_CP1_CI_AS",
            "memory": {
                "minimum": "64GB",
                "recommended": "128GB",
                "notes": "Set max server memory to 80% of available RAM"
            },
            "storage": {
                "data_files": "500GB minimum for production",
                "log_files": "100GB minimum",
                "tempdb": "50GB minimum",
                "notes": "Use separate drives for data, logs, and tempdb"
            },
            "configuration": {
                "max_degree_of_parallelism": 4,
                "cost_threshold_for_parallelism": 50,
                "recovery_model": "FULL for production",
                "notes": "Optimize for OLTP workloads"
            },
            "notes": "Refer to Oracle Certifications for exact version compatibility"
        },
        "oracle_db": {
            "versions": [
                "Oracle Database 19c",
                "Oracle Database 21c"
            ],
            "character_set": "AL32UTF8",
            "memory": {
                "sga_target": "32GB minimum",
                "pga_aggregate_target": "8GB minimum"
            },
            "tablespaces": [
                "JDE_DATA",
                "JDE_INDEX",
                "JDE_LOB"
            ],
            "notes": "Oracle Database is recommended for large enterprise deployments"
        }
    }
}

# ============================================================================
# INSTALLATION SEQUENCE
# ============================================================================

INSTALLATION_SEQUENCE = {
    "production": [
        {
            "step": 1,
            "phase": "Pre-Installation",
            "action": "Complete Environment Assessment",
            "details": [
                "Verify all server hardware meets requirements",
                "Confirm network connectivity between all servers",
                "Validate database connectivity and permissions",
                "Review Oracle Certifications for version compatibility"
            ],
            "duration": "1-2 hours",
            "critical": True
        },
        {
            "step": 2,
            "phase": "Pre-Installation",
            "action": "Backup Existing Setup",
            "details": [
                "Backup Deployment Server directories: /System, /Systemcomp, /OneWorld Client Install",
                "Export all JDE database schemas",
                "Backup Server Manager configuration",
                "Document current environment settings",
                "Create system restore point"
            ],
            "duration": "2-4 hours",
            "critical": True,
            "rollback_point": True
        },
        {
            "step": 3,
            "phase": "Prerequisites",
            "action": "Install Runtime Prerequisites",
            "details": [
                "Install Microsoft Visual C++ 2010/2012/2013 Runtime X86 Redistributables",
                "Install .NET Framework 4.8",
                "Configure Windows Firewall rules",
                "Set up service accounts"
            ],
            "duration": "1 hour",
            "critical": True
        },
        {
            "step": 4,
            "phase": "Core Installation",
            "action": "Install JDE Tools Release 9.2 via Server Manager",
            "details": [
                "Download Tools Release from Oracle Software Delivery Cloud",
                "Launch Server Manager installation wizard",
                "Select 'Install JD Edwards EnterpriseOne Tools'",
                "Configure installation paths",
                "Complete installation and verify"
            ],
            "duration": "2-3 hours",
            "critical": True,
            "server_manager_task": True
        },
        {
            "step": 5,
            "phase": "Core Installation",
            "action": "Convert Local Database Encryption",
            "details": [
                "Navigate to Deployment Server installation directory",
                "Run ReconfigureDB.exe",
                "Follow prompts to convert encryption",
                "Verify database connectivity after conversion"
            ],
            "duration": "30 minutes",
            "critical": True,
            "command": "ReconfigureDB.exe"
        },
        {
            "step": 6,
            "phase": "Patching",
            "action": "Install Planner ESU (Bug 26501747)",
            "details": [
                "Download Bug 26501747 from My Oracle Support",
                "Run self-extracting executable",
                "Follow HTML special instructions document",
                "Verify installation via Server Manager"
            ],
            "duration": "1-2 hours",
            "critical": True,
            "mos_reference": "Bug 26501747"
        },
        {
            "step": 7,
            "phase": "Patching",
            "action": "Apply Current Tools Rollup ESU",
            "details": [
                "Check My Oracle Support for latest Tools Rollup",
                "Download applicable rollup for Tools 9.2.x",
                "Deploy via Server Manager ESU deployment",
                "Follow any special instructions"
            ],
            "duration": "2-3 hours",
            "critical": True,
            "mos_reference": "Check MOS for current Bug number"
        },
        {
            "step": 8,
            "phase": "Application Updates",
            "action": "Install Tools Application Enhancement Rollup ASU",
            "details": [
                "Download ASU from Oracle Software Delivery Cloud",
                "Uncompress ASU package on Deployment Server",
                "Use Server Manager to deploy ASU",
                "Navigate to P96470 (GH9612) for application deployment",
                "Deploy to all environments in sequence (DEV -> TEST -> PROD)"
            ],
            "duration": "3-4 hours",
            "critical": True,
            "menu_navigation": "GH9612 > P96470"
        },
        {
            "step": 9,
            "phase": "Post-Installation",
            "action": "Deploy Automated Special Instructions (ASI)",
            "details": [
                "Select package in Server Manager",
                "Deploy ASI components",
                "Run post-install UBEs (R98222UDO, etc.)",
                "Verify ASI deployment status"
            ],
            "duration": "1-2 hours",
            "critical": True
        },
        {
            "step": 10,
            "phase": "Verification",
            "action": "Complete Installation Verification",
            "details": [
                "Verify fixes via Oracle Product Features",
                "Test environment sign-on for all users",
                "Validate batch processing functionality",
                "Test web client access",
                "Verify AIS services (if applicable)",
                "Run functional smoke tests"
            ],
            "duration": "2-4 hours",
            "critical": True
        }
    ],
    "test_py": [
        {
            "step": 1,
            "phase": "Pre-Installation",
            "action": "Validate Test Environment Infrastructure",
            "details": [
                "Confirm test server meets minimum requirements",
                "Verify network isolation from production (if required)",
                "Set up test database instance"
            ],
            "duration": "1 hour",
            "critical": True
        }
    ],
    "development": [
        {
            "step": 1,
            "phase": "Pre-Installation",
            "action": "Set Up Development Infrastructure",
            "details": [
                "Configure development server",
                "Set up version control integration",
                "Configure Object Management Workbench (OMW)"
            ],
            "duration": "2 hours",
            "critical": True
        }
    ],
    "standalone_demo": [
        {
            "step": 1,
            "phase": "Installation",
            "action": "Install Standalone Demo",
            "details": [
                "Download demo image from Oracle",
                "Configure VM settings",
                "Import and configure demo environment"
            ],
            "duration": "4-6 hours",
            "critical": True,
            "notes": "Standalone demo is for evaluation only - not for production use"
        }
    ]
}
