"""
Configuration file for Okta Identity Automation Lab
"""

# Okta Configuration
OKTA_CONFIG = {
    "ORG_URL": "https://your-org.okta.com",
    "API_TOKEN": "your-api-token-here",
    "AUTH_METHOD": "api_token",  # Options: api_token, oauth2
}

# SCIM Configuration
SCIM_CONFIG = {
    "ENABLED": True,
    "API_VERSION": "v2",
    "BATCH_SIZE": 100,
    "SYNC_INTERVAL": 3600,  # seconds
}

# MFA Configuration
MFA_CONFIG = {
    "REQUIRED_FOR_ALL": False,
    "REQUIRED_FACTORS": ["OKTA", "SMS"],
    "CHALLENGE_TIMEOUT": 300,  # seconds
    "MAX_ATTEMPTS": 3,
}

# Zero Trust Configuration
ZERO_TRUST_CONFIG = {
    "ENABLED": True,
    "MINIMUM_TRUST_SCORE": 0.5,
    "ENFORCE_MFA_FOR_SENSITIVE_RESOURCES": True,
    "TRUSTED_NETWORKS": [
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
    ],
    "ANOMALY_DETECTION": {
        "ENABLED": True,
        "SENSITIVITY": "medium",  # low, medium, high
    },
}

# RBAC Configuration
RBAC_CONFIG = {
    "ROLE_HIERARCHY_ENABLED": True,
    "PERMISSION_INHERITANCE": True,
    "DEFAULT_ROLE": "employee",
}

# Identity Lifecycle Configuration
LIFECYCLE_CONFIG = {
    "ONBOARDING_WORKFLOW": {
        "STAGES": [
            "CREATE",
            "PROVISION",
            "ACTIVATE",
            "NOTIFY_MANAGER",
        ],
    },
    "OFFBOARDING_WORKFLOW": {
        "STAGES": [
            "SUSPEND",
            "REVOKE_ACCESS",
            "DEPROVISION",
            "ARCHIVE",
        ],
    },
    "INACTIVE_USER_THRESHOLD": 90,  # days
}

# Logging Configuration
LOGGING_CONFIG = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "AUDIT_LOG_ENABLED": True,
    "AUDIT_LOG_RETENTION": 365,  # days
}

# Feature Flags
FEATURES = {
    "SCIM_PROVISIONING": True,
    "SSO_INTEGRATION": True,
    "MFA_ENFORCEMENT": True,
    "ZERO_TRUST_AUTH": True,
    "RBAC_MANAGEMENT": True,
    "LIFECYCLE_AUTOMATION": True,
    "AUDIT_LOGGING": True,
}
