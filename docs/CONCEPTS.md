# Identity Management Concepts

This document explains the core identity management concepts implemented in this project.

## Table of Contents

1. [Single Sign-On (SSO)](#single-sign-on-sso)
2. [Multi-Factor Authentication (MFA)](#multi-factor-authentication-mfa)
3. [Identity Provisioning](#identity-provisioning)
4. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
5. [Zero Trust Security](#zero-trust-security)
6. [Identity Lifecycle](#identity-lifecycle)

## Single Sign-On (SSO)

### Definition

Single Sign-On allows users to authenticate once and gain access to multiple applications without re-authenticating.

### Benefits

- **Improved User Experience** - Users remember one password
- **Reduced Support Costs** - Fewer password resets
- **Enhanced Security** - Centralized password management
- **Better Compliance** - Centralized audit logging
- **Easier Offboarding** - Single point of revocation

### Protocols

#### OAuth 2.0

**Authorization Protocol**

- Designed for delegation
- Used for authorization
- Token-based
- Stateless

**Grant Types:**

- Authorization Code - Web applications
- Client Credentials - Service-to-service
- Resource Owner Password - Legacy applications
- Implicit - Single-page applications (deprecated)
- Refresh Token - Token renewal

**Flow:**

```
1. User clicks "Sign In"
2. App redirects to authorization endpoint
3. User logs in to Okta
4. Okta redirects back with authorization code
5. App exchanges code for tokens (backend)
6. App receives tokens
7. App creates session
```

#### OpenID Connect (OIDC)

**Authentication Protocol built on OAuth 2.0**

- Adds identity layer to OAuth 2.0
- Returns ID token (JWT with user claims)
- Access token for API access

**Key Differences from OAuth 2.0:**

- ID token contains user information
- UserInfo endpoint for user attributes
- Standard claims (name, email, etc.)

**Typical Claims in ID Token:**

```json
{
  "iss": "https://org.okta.com",
  "sub": "user001",
  "aud": "application_id",
  "iat": 1633024800,
  "exp": 1633028400,
  "auth_time": 1633024800,
  "name": "John Doe",
  "email": "john@company.com",
  "groups": ["engineering", "staff"]
}
```

#### SAML 2.0

**XML-based Security Assertion Markup Language**

- Enterprise standard
- XML assertions
- Both authentication and authorization
- Identity Provider (IdP) initiated

**Key Components:**

- Service Provider (SP) - Application
- Identity Provider (IdP) - Okta
- Assertion - Signed XML containing user data

**SAML Assertion:**

```xml
<saml:Assertion IssueInstant="2024-03-15T10:30:00Z" ID="..." Version="2.0">
  <saml:Issuer>https://org.okta.com</saml:Issuer>
  <saml:Subject>
    <saml:NameID>john.doe@company.com</saml:NameID>
  </saml:Subject>
  <saml:AttributeStatement>
    <saml:Attribute Name="email" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
      <saml:AttributeValue>john.doe@company.com</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="groups">
      <saml:AttributeValue>engineering</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

### OAuth 2.0 vs SAML 2.0

| Aspect         | OAuth 2.0     | SAML 2.0                       |
| -------------- | ------------- | ------------------------------ |
| Purpose        | Authorization | Authentication & Authorization |
| Format         | JSON tokens   | XML assertions                 |
| Complexity     | Simpler       | More complex                   |
| Mobile Support | Better        | Limited                        |
| API Protection | Excellent     | Limited                        |
| Enterprise     | Growing       | Established                    |

## Multi-Factor Authentication (MFA)

### Definition

Multi-factor authentication requires users to provide multiple verification methods to prove their identity.

### Factors Categories

#### Knowledge Factor (Something you know)

- Password
- PIN
- Security questions

#### Possession Factor (Something you have)

- Hardware token
- Smart card
- Mobile phone
- USB security key

#### Inherence Factor (Something you are)

- Fingerprint
- Face recognition
- Voice recognition
- Iris scan

#### Location/Behavior Factor

- IP address location
- Device location
- Typing patterns
- Device behavior

### MFA Methods

#### OKTA Verify

- Mobile app on user's phone
- Push notification approval
- Time-based one-time password (TOTP)
- Biometric unlock

#### Google Authenticator

- TOTP-based
- 6-digit codes every 30 seconds
- Works offline
- Restore tokens

#### SMS

- One-time passcode sent via SMS
- Low cost
- Universal phone support
- Less secure (SMS interception)

#### Email

- One-time passcode sent via email
- User controls delivery
- Easy recovery

#### Hardware Token

- Physical device
- TOTP or challenge-response
- High security
- No battery concerns on TOTP tokens

#### Duo Security

- Push notifications
- Touchid/Face ID
- Passcode backup
- Geo-location verification

### Adaptive MFA

**Dynamic MFA based on Risk Assessment:**

```
Risk Assessment:
├─ User Factor
│  ├─ First time user? (High risk)
│  ├─ Unusual device? (High risk)
│  ├─ Known user? (Low risk)
│
├─ Location Factor
│  ├─ New location? (High risk)
│  ├─ Impossible travel? (Highest risk)
│  ├─ Familiar location? (Low risk)
│
├─ Device Factor
│  ├─ Trusted device? (Low risk)
│  ├─ New device? (High risk)
│  ├─ Compromised device? (Highest risk)
│
├─ Network Factor
│  ├─ VPN usage? (Medium risk)
│  ├─ Tor network? (High risk)
│  ├─ Office network? (Low risk)

MFA Requirement:
├─ Risk Score < 0.3: No additional MFA
├─ Risk Score 0.3-0.7: Standard MFA
├─ Risk Score > 0.7: Step-up authentication (multiple factors)
```

## Identity Provisioning

### Definition

Identity provisioning is the process of creating, updating, and deleting user accounts across systems.

### Types

#### User Provisioning

Creating user accounts in applications when users join organization.

**Process:**

1. HR creates employee
2. SCIM API receives notification
3. User created in Okta
4. Credentials generated
5. Applications notified
6. Account created in apps
7. Welcome email sent

#### Group Provisioning

Creating and managing groups across systems.

**Process:**

1. Define group in Okta (e.g., "Engineering")
2. Add users to group
3. SCIM pushes group to applications
4. Applications receive group membership
5. User inherits group permissions

#### Entitlement Provisioning

Assigning applications and roles to users.

**Process:**

1. User assigned to role in Okta
2. Role includes applications
3. SCIM assigns applications
4. Applications grant access
5. User sees app in app launcher

### Provisioning Methods

#### Pull-based (Application pulls from Okta)

- Application periodically queries Okta
- Application caches data
- Less real-time
- Better app control

#### Push-based (Okta pushes to Application)

- Okta initiates changes
- Real-time updates
- More timely
- Okta controls flow

#### SCIM (System for Cross-domain Identity Management)

- Standard provisioning protocol
- REST API based
- Bi-directional
- Standardized operations

**SCIM Operations:**

```
CREATE:  POST /scim/v2/Users
GET:     GET /scim/v2/Users/{id}
UPDATE:  PUT /scim/v2/Users/{id}
PATCH:   PATCH /scim/v2/Users/{id}
DELETE:  DELETE /scim/v2/Users/{id}
LIST:    GET /scim/v2/Users?filter=...
```

### Deprovisioning

Removing user access when they leave organization.

**Process:**

1. HR marks employee as terminated
2. SCIM notification sent
3. User suspended in Okta
4. Groups removed
5. Applications revoke access
6. Email disabled
7. VPN access removed
8. Physical access cards disabled
9. Equipment collected
10. Final data archival

## Role-Based Access Control (RBAC)

### Definition

RBAC is a method of regulating access based on user roles rather than individual permissions.

### Components

#### Role

Collection of permissions assigned to users.

**Example: Software Engineer Role**

```
Role: Software Engineer
Permissions:
  - View repository
  - Create branches
  - Submit pull requests
  - Read CI/CD logs
  - Deploy to staging
```

#### Permission

Specific action on a specific resource.

**Example: "View Repository"**

```
Permission: View Repository
Resource: GitHub Repository
Action: READ
Constraints:
  - Repository: engineering/*
  - Time: 9 AM - 6 PM
  - Location: Office or VPN
```

#### User

Entity assigned roles for access.

**Example:**

```
User: john.doe
Assigned Roles:
  - Software Engineer
  - Team Lead
  - On-call Responder
```

### Role Hierarchy

Roles can inherit from parent roles.

```
Administrator Role
├─ Manage Users (permission)
├─ Manage Groups (permission)
├─ Manage Applications (permission)
└── Senior Engineer Role (parent)
    ├─ View All Reports (permission)
    ├─ Create Reports (permission)
    └── Software Engineer Role (parent)
        ├─ View Repository (permission)
        ├─ Create Branches (permission)
        └─ Submit PRs (permission)
```

**Permission Resolution:**

- Administrator inherits Senior Engineer permissions
- Senior Engineer inherits Software Engineer permissions
- Explicit permissions override inherited ones

### Access Control Decision

```
User requests access to resource

1. Get user's roles
   user.roles = [Software Engineer, Team Lead]

2. Get permissions from roles
   software_engineer.permissions = [view_repo, create_branch, ...]
   team_lead.permissions = [view_team_metrics, manage_team, ...]

3. Combine permissions
   user_permissions = {view_repo, create_branch, view_team_metrics, manage_team}

4. Check if user has required permission
   IF update_repository IN user_permissions
      ALLOW
   ELSE
      DENY
```

### Principle of Least Privilege

Users have minimum permissions needed for their role.

**Benefits:**

- Reduces attack surface
- Limits damage from compromised account
- Improves compliance
- Reduces accidental changes

## Zero Trust Security

### Definition

Security model assuming no inherent trust. Every access request must be verified.

### Principles

1. **Verify Every Access** - Never trust by default
2. **Assume Breach** - Plan for worst-case scenario
3. **Secure Every Device** - Endpoint protection essential
4. **Inspect and Log Everything** - Complete visibility
5. **Automate Response** - Fast detection and response

### Zero Trust Architecture

```
Every Access Request Must Pass Multiple Checks:

1. Identity Verification
   ├─ Who are you? (Authentication)
   ├─ MFA challenge if needed
   └─ Session validation

2. Device Assessment
   ├─ Is device trusted?
   ├─ Device compliance check
   ├─ Antivirus status
   ├─ Encryption enabled?
   └─ OS patches current?

3. Network Evaluation
   ├─ What network are you on?
   ├─ IP reputation check
   ├─ VPN detection
   ├─ Geographic location
   └─ Network anomalies?

4. Contextual Analysis
   ├─ Is this normal behavior?
   ├─ Unusual time of access?
   ├─ Unusual resource access?
   ├─ Impossible travel detected?
   └─ Anomaly score

5. Authorization Check
   ├─ Do you have permission? (RBAC)
   ├─ Attribute-based control
   ├─ Conditional policies
   └─ Time-based access

6. Decision Engine
   ├─ Calculate trust score
   ├─ Apply policies
   ├─ Make ALLOW/DENY/CHALLENGE decision
   └─ Log decision
```

### Trust Score Calculation

```
Overall Trust Score =
  User_Identity (10%) +
  Device_Trust (20%) +
  Network_Trust (15%) +
  Resource_Sensitivity_Factor (20%) +
  Time_Risk_Factor (10%) +
  Behavior_Analysis (25%)

Score Range: 0.0 - 1.0

Decision Logic:
  Score >= 0.8 : ALLOW
  Score 0.5-0.8: CONDITIONAL_ALLOW (MFA required)
  Score < 0.5  : DENY (Manual review required)
```

### Continuous Verification

Verification doesn't end with login.

**Continuous Checks:**

- Monitor user activity
- Detect behavior changes
- Revoke access immediately if needed
- Re-evaluate permissions
- Update risk scores

## Identity Lifecycle

### Complete User Journey

#### Stage 1: Pre-Hire (Day -30)

```
- Job offer issued
- Candidate details collected
- Background check initiated
- Equipment ordered
- Workspace prepared
```

#### Stage 2: Day 1 Onboarding

```
- Employee created in HR system
- SCIM provisioning triggered
- Okta account created
- Initial password generated
- Email account created
- Welcome email sent
```

#### Stage 3: First Week

```
- MFA enrollment
- Training materials provided
- Application access granted
- Group memberships assigned
- Manager assignment confirmed
- Team introductions
```

#### Stage 4: Active Employment

```
- Regular access reviews
- Role changes (promotions, transfers)
- Permission updates
- MFA factor management
- Access pattern monitoring
```

#### Stage 5: Offboarding (Last Day)

```
- Termination notification
- Access review
- Manager notification
- Equipment collected
- Workspace cleared
- Final access review
```

#### Stage 6: Post-Offboarding

```
- User deprovisioned
- All access revoked
- Data archived
- Account marked as inactive
- Final audit log

Timeline:
  Day 0: Terminate
  Hour 1: Suspend Okta account
  Hour 2: Revoke SSO access
  Hour 4: Remove from groups
  Day 1: Disable email
  Day 5: Revoke VPN
  Day 7: Remove from applications
  Day 30: Delete account
  Year 1: Archive data
  Year 7: Delete archived data
```

### Lifecycle Events

```
User Lifecycle Events:
├─ HIRED: Employee created in HR
├─ PROVISIONED: Okta account created
├─ ACTIVATED: Account ready to use
├─ MFA_ENROLLED: MFA factor registered
├─ FIRST_LOGIN: User's first login
├─ ROLE_CHANGED: Role assignment changed
├─ TRANSFERRED: Department changed
├─ PROMOTED: Promoted to new role
├─ SUSPENDED: Administrative leave
├─ REACTIVATED: Returned from leave
├─ TERMINATED: Employment ended
├─ DEPROVISIONED: Access revoked
├─ ARCHIVED: Data archived
└─ DELETED: Account permanently deleted
```

### Access Review Process

**Quarterly Access Review:**

```
1. Manager receives list of user's access
2. Manager verifies each access is needed
3. Manager removes unnecessary access
4. Manager approves required access
5. System enforces changes
6. Audit log captures review
```

## References

- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [SAML 2.0 Specification](https://wiki.oasis-open.org/security/SAML-2-0-Web-Browser-SSO-Profile)
- [SCIM 2.0 Specification](https://tools.ietf.org/html/rfc7643)
- [Zero Trust Architecture (NIST)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [NIST SP 800-63B Authentication](https://pages.nist.gov/800-63-3/sp800-63b.html)
