# Okta Identity Automation Lab

Enterprise-grade identity architecture demonstration using Okta. This project showcases solution architect-level capabilities in implementing secure, scalable identity management for enterprises.

## Overview

The Okta Identity Automation Lab demonstrates core enterprise identity concepts and how they work together to create a secure, automated identity and access management (IAM) system.

### Key Capabilities

- **Single Sign-On (SSO)** - OAuth 2.0 / OIDC and SAML 2.0 integration
- **Multi-Factor Authentication (MFA)** - Adaptive MFA policies and enforcement
- **SCIM Provisioning** - Automated user and group provisioning from HR systems
- **Identity Lifecycle Automation** - Complete onboarding/offboarding workflows
- **Role-Based Access Control (RBAC)** - Enterprise role hierarchy and permission management
- **Zero Trust Authentication** - Context-aware access decisions with continuous verification

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Enterprise Applications                      │
│                   (Web, Mobile, SaaS, APIs)                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Okta Platform    │
                    │  (Identity Hub)    │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    ┌────────┐         ┌────────────┐         ┌──────────┐
    │  SSO   │         │   MFA      │         │ Lifecycle│
    │ (OIDC) │         │ Enforcement│         │Management│
    └────────┘         └────────────┘         └──────────┘
        │                      │                      │
        ▼                      ▼                      ▼
    ┌──────────────────────────────────────────────────────┐
    │           Zero Trust Engine                          │
    │  (Adaptive Access, Device Trust, Network Evaluation) │
    └──────────────────────────────────────────────────────┘
        │
        ▼
    ┌──────────────────────────────────────────────────────┐
    │     RBAC Manager                                     │
    │     (Roles, Permissions, Authorization)             │
    └──────────────────────────────────────────────────────┘
        │
        ▼
    ┌──────────────────────────────────────────────────────┐
    │     SCIM Provisioning                                │
    │     (HR Integration, User Sync, Group Management)    │
    └──────────────────────────────────────────────────────┘
```

## Project Structure

```
okta-identity-automation-lab/
├── src/
│   ├── __init__.py
│   ├── okta_client.py           # Core Okta API client
│   ├── mfa_manager.py           # Multi-factor authentication
│   ├── identity_lifecycle.py    # User provisioning/deprovisioning
│   ├── rbac_manager.py          # Role-based access control
│   ├── zero_trust.py            # Zero trust authentication
│   └── scim_provisioning.py     # SCIM 2.0 provisioning
├── examples/
│   ├── 01_complete_lifecycle.py # Complete onboarding/offboarding
│   ├── 02_scim_provisioning.py  # HR system integration
│   └── 03_sso_applications.py   # SSO & application setup
├── configs/
│   ├── config.py                # Configuration settings
│   └── .env.example             # Environment variables template
├── docs/
│   ├── ARCHITECTURE.md          # Detailed architecture docs
│   ├── CONCEPTS.md              # Identity management concepts
│   └── API_REFERENCE.md         # API documentation
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Core Modules

### 1. Okta Client (`okta_client.py`)

Core client for interacting with Okta APIs. Handles authentication, user management, and lifecycle operations.

**Key Classes:**
- `OktaClient` - Main API client
- `OktaConfig` - Configuration management

**Key Methods:**
- User management: `create_user()`, `get_user()`, `update_user()`, `delete_user()`
- Group management: `create_group()`, `add_user_to_group()`, `remove_user_from_group()`
- Authentication: `enable_factor()`, `list_user_factors()`
- Applications: `create_app()`, `list_apps()`
- Policies: `create_access_policy()`, `list_policies()`

### 2. MFA Manager (`mfa_manager.py`)

Manages multi-factor authentication policies and user factor enrollment.

**Key Classes:**
- `MFAManager` - MFA policy and enrollment management
- `MFAPolicy` - MFA policy definition
- `MFAFactorType` - Supported MFA factors (OKTA, GOOGLE, DUO, SMS, EMAIL, HARDWARE_TOKEN)

**Key Methods:**
- `create_policy()` - Define MFA policies
- `register_user_factor()` - Enroll user in MFA
- `verify_factor()` - Verify MFA factor
- `enforce_mfa_for_group()` - Apply policy to groups

### 3. Identity Lifecycle (`identity_lifecycle.py`)

Manages complete user lifecycle from provisioning to deprovisioning.

**Key Classes:**
- `IdentityLifecycleManager` - Lifecycle workflow management
- `UserProfile` - User with lifecycle state
- `UserStatus` - User status enum (ACTIVE, STAGING, PROVISIONED, DEPROVISIONED, SUSPENDED)
- `LifecycleEvent` - Lifecycle event types

**Key Methods:**
- `create_user()` - Create new user (onboarding starts)
- `provision_user()` - Provision resources
- `activate_user()` - Activate user account
- `suspend_user()` - Suspend user (administrative leave)
- `deprovision_user()` - Revoke access (offboarding)
- `delete_user()` - Permanently delete user

### 4. RBAC Manager (`rbac_manager.py`)

Manages roles, permissions, and access control.

**Key Classes:**
- `RBACManager` - Role-based access control
- `Role` - Role definition
- `Permission` - Permission definition

**Key Methods:**
- `create_permission()` - Define permission
- `create_role()` - Create role with permissions
- `assign_role_to_user()` - Assign role to user
- `has_resource_access()` - Check user access to resource
- `set_role_hierarchy()` - Define role parent relationships

### 5. Zero Trust Engine (`zero_trust.py`)

Implements zero trust principles with context-aware access evaluation.

**Key Classes:**
- `ZeroTrustEngine` - Zero trust authentication engine
- `AccessRequest` - Access request for evaluation
- `TrustLevel` - Trust level enum

**Key Methods:**
- `evaluate_access()` - Evaluate access request
- `register_device()` - Trust a device
- `add_trusted_network()` - Add trusted network
- `require_mfa_for_resource()` - Require MFA for resource
- `audit_access_log()` - Get access audit log

**Evaluation Factors:**
- User Identity (10%)
- Device Trust (20%)
- Network Trust (15%)
- Resource Sensitivity (20%)
- Time-based Risk (10%)
- Behavior Analysis (25%)

### 6. SCIM Provisioning (`scim_provisioning.py`)

Implements SCIM 2.0 protocol for automated provisioning.

**Key Classes:**
- `SCIMProvisioningManager` - SCIM provisioning management
- `SCIMUser` - SCIM 2.0 user representation
- `SCIMGroup` - SCIM 2.0 group representation

**Key Methods:**
- `create_user()` - Create user via SCIM
- `batch_upsert_users()` - Bulk provisioning
- `sync_from_hr_system()` - Sync users from HR
- `create_group()` - Create group
- `add_member_to_group()` - Add group membership

## Usage Examples

### Example 1: Complete Identity Lifecycle

```bash
python examples/01_complete_lifecycle.py
```

Demonstrates:
- User onboarding (creation, provisioning, activation)
- Role assignment and RBAC
- MFA enrollment and verification
- Zero trust access evaluation
- User offboarding (suspension, deprovisioning)

### Example 2: SCIM Provisioning

```bash
python examples/02_scim_provisioning.py
```

Demonstrates:
- User creation via SCIM
- Bulk provisioning from HR system
- Group management
- User list and pagination
- Update and delete operations

### Example 3: SSO and Applications

```bash
python examples/03_sso_applications.py
```

Demonstrates:
- OIDC and SAML application setup
- OAuth 2.0 authorization flow
- Token claims and user identity
- Single logout (SLO)
- Security best practices

## Configuration

1. Copy the configuration template:
```bash
cp configs/.env.example configs/.env
```

2. Edit `configs/.env` with your Okta credentials:
```
OKTA_ORG_URL=https://your-org.okta.com
OKTA_API_TOKEN=your-api-token-here
```

3. Configure application settings in `configs/config.py`

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/okta-identity-automation-lab.git
cd okta-identity-automation-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Examples

```bash
# Run all examples
python examples/01_complete_lifecycle.py
python examples/02_scim_provisioning.py
python examples/03_sso_applications.py
```

## Key Enterprise Identity Concepts

### Single Sign-On (SSO)

Enables users to access multiple applications with a single set of credentials using OAuth 2.0, OIDC, or SAML protocols.

**Benefits:**
- Improved user experience
- Reduced password fatigue
- Centralized authentication
- Enhanced security through token-based auth

### Multi-Factor Authentication (MFA)

Requires users to provide multiple verification factors for increased security.

**Factors:**
- Knowledge (password)
- Possession (phone, hardware token)
- Inherence (biometrics)

### SCIM Provisioning

System for Cross-domain Identity Management enables automated user and group provisioning from HR systems.

**Key Operations:**
- Create/update/delete users
- Manage group memberships
- Bulk provisioning
- Bi-directional synchronization

### Identity Lifecycle Automation

Automates identity management from hire to retire.

**Stages:**
- **Onboarding**: Create account, provision resources, activate
- **Active**: User managing access and permissions
- **Offboarding**: Suspend, revoke access, deprovision, archive

### Role-Based Access Control (RBAC)

Implements principle of least privilege by assigning roles to users rather than individual permissions.

**Components:**
- Roles: Collections of permissions
- Permissions: Specific actions on resources
- Role Hierarchy: Parent-child role relationships
- Users: Assigned roles for access

### Zero Trust Authentication

Modern security model assuming no inherent trust. Every access request is evaluated based on context.

**Principles:**
- Never trust by default, always verify
- Verify user identity
- Assess device health
- Evaluate network
- Evaluate resource sensitivity
- Consider behavior patterns
- Require MFA for sensitive resources

## Security Best Practices

1. **API Token Management**
   - Rotate tokens regularly
   - Store tokens securely (never in code)
   - Use environment variables

2. **Token Security**
   - Validate token signatures using JWKS
   - Check token expiration
   - Validate audience claim

3. **MFA Enforcement**
   - Require MFA for all users
   - Implement adaptive MFA
   - Monitor MFA enrollment

4. **Access Control**
   - Implement principle of least privilege
   - Review RBAC regularly
   - Monitor permission usage

5. **Audit Logging**
   - Log all identity operations
   - Retain logs for compliance
   - Monitor for anomalies

## Integration Points

This project demonstrates integration with:

- **HR Systems** - Employee data synchronization
- **Applications** - OIDC/SAML SSO
- **Identity APIs** - Okta REST APIs
- **Device Management** - Trust device identity
- **Network Security** - IP trust evaluation

## Solution Architect Skills Demonstrated

1. **Enterprise Architecture**
   - Multi-layer identity architecture
   - Integration patterns
   - Security by design

2. **Identity & Access Management**
   - SSO protocols (OIDC, SAML, OAuth 2.0)
   - MFA strategies
   - RBAC implementation
   - Zero trust architecture

3. **System Design**
   - Lifecycle automation
   - Batch provisioning
   - Audit logging
   - Error handling

4. **Security**
   - Zero trust principles
   - Token security
   - MFA enforcement
   - Risk assessment

5. **API Design**
   - RESTful principles
   - Error handling
   - Extensibility
   - Documentation

## Production Considerations

When deploying to production:

1. **Security**
   - Use managed secrets (AWS Secrets Manager, etc.)
   - Implement rate limiting
   - Add request signing
   - Audit all operations

2. **Scalability**
   - Implement caching
   - Use async operations
   - Implement retry logic
   - Monitor performance

3. **High Availability**
   - Multiple Okta orgs
   - Failover logic
   - Health checks
   - Circuit breakers

4. **Compliance**
   - Audit logging
   - Data retention policies
   - Access logging
   - Encryption in transit/rest

## API Reference

Detailed API documentation available in [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

## Architecture Documentation

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Contributing

Contributions welcome! Please ensure:
- Code follows PEP 8 style guide
- Functions have docstrings
- Error handling is comprehensive
- Examples demonstrate functionality

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, open a GitHub issue or contact the project maintainers.

## References

- [Okta Developer Documentation](https://developer.okta.com/)
- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [SCIM 2.0 Specification](https://tools.ietf.org/html/rfc7643)
- [SAML 2.0 Specification](https://wiki.oasis-open.org/security/SAML-2-0-Web-Browser-SSO-Profile)
- [Zero Trust Architecture (NIST)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
