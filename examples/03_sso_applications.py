"""
Example: Enterprise SSO and Application Integration
Demonstrates Single Sign-On and OIDC/SAML application setup
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.okta_client import OktaClient, OktaConfig, AuthMethod
import json


def example_sso_and_applications():
    """Enterprise SSO and application integration example"""
    print("=" * 80)
    print("ENTERPRISE SSO & APPLICATION INTEGRATION")
    print("=" * 80)

    # Note: For actual usage, replace with real Okta org details
    # This example demonstrates the API structure and capabilities
    print("\nNOTE: This example shows the API structure.")
    print("For production use, configure with real Okta credentials in .env file\n")

    # Mock Okta configuration (in production, load from environment)
    config = OktaConfig(
        org_url="https://example.okta.com",
        api_token="00-demo-token-for-example",
        auth_method=AuthMethod.API_TOKEN,
    )

    print("1. OKTA CLIENT INITIALIZATION")
    print("-" * 80)
    print(f"✓ Configured Okta Org: {config.org_url}")
    print(f"✓ Auth Method: {config.auth_method.value}")

    # In production, create actual client
    # client = OktaClient(config)

    print("\n2. APPLICATION INTEGRATION EXAMPLES")
    print("-" * 80)

    # Example OIDC application structure
    oidc_app = {
        "name": "oidc_client_custom_app",
        "label": "Custom Web Application",
        "signOnMode": "OPENID_CONNECT",
        "settings": {
            "oauthClient": {
                "client_type": "public",
                "redirect_uris": [
                    "http://localhost:8080/callback",
                    "https://app.example.com/callback",
                ],
                "response_types": ["code", "token", "id_token"],
                "grant_types": ["authorization_code", "refresh_token", "implicit"],
                "application_type": "web",
            }
        },
    }

    print("✓ OIDC Application Configuration:")
    print(f"  Label: {oidc_app['label']}")
    print(f"  Sign-On Mode: {oidc_app['signOnMode']}")
    print(f"  Redirect URIs: {len(oidc_app['settings']['oauthClient']['redirect_uris'])}")
    print(f"  Grant Types: {', '.join(oidc_app['settings']['oauthClient']['grant_types'])}")

    # Example SAML application structure
    saml_app = {
        "name": "saml_service_provider",
        "label": "SAML Service Provider",
        "signOnMode": "SAML_2_0",
        "settings": {
            "signOn": {
                "defaultRelayState": "",
                "ssoAcsUrl": "https://app.example.com/saml/acs",
                "idpIssuer": "https://example.okta.com",
                "audience": "https://app.example.com/saml",
                "recipient": "https://app.example.com/saml/acs",
                "destination": "https://app.example.com/saml/acs",
                "subjectNameIdFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
                "requestCompressed": False,
                "authnContextClassRef": "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport",
            },
            "app": {
                "samlVersion": "2.0",
            },
        },
    }

    print("\n✓ SAML Application Configuration:")
    print(f"  Label: {saml_app['label']}")
    print(f"  Sign-On Mode: {saml_app['signOnMode']}")
    print(f"  ACS URL: {saml_app['settings']['signOn']['ssoAcsUrl']}")
    print(f"  Audience: {saml_app['settings']['signOn']['audience']}")

    print("\n3. SSO FLOW - AUTHORIZATION CODE FLOW")
    print("-" * 80)

    sso_flow = {
        "flow": "Authorization Code Flow",
        "steps": [
            "1. User clicks 'Sign In' on app",
            "2. App redirects to Okta authorization endpoint",
            "3. User enters credentials",
            "4. Okta validates MFA if required",
            "5. User grants consent",
            "6. Okta redirects back with authorization code",
            "7. App exchanges code for tokens (backend)",
            "8. Okta returns ID token and access token",
            "9. App validates token and creates session",
            "10. User logged in to app",
        ],
    }

    print("✓ OAuth 2.0 / OIDC Authorization Code Flow:")
    for step in sso_flow["steps"]:
        print(f"  {step}")

    print("\n4. USER IDENTITY & CLAIMS")
    print("-" * 80)

    id_token_claims = {
        "iss": "https://example.okta.com",
        "sub": "user001",
        "aud": "0oabcdefg123456",
        "iat": 1633024800,
        "exp": 1633028400,
        "auth_time": 1633024800,
        "name": "John Doe",
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@company.com",
        "email_verified": True,
        "groups": ["engineering", "staff"],
    }

    print("✓ ID Token Claims (JWT):")
    for key, value in id_token_claims.items():
        if key != "groups":
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")

    access_token_claims = {
        "iss": "https://example.okta.com",
        "sub": "user001",
        "aud": "https://api.example.com",
        "iat": 1633024800,
        "exp": 1633028400,
        "scope": "openid profile email groups",
        "scp": ["openid", "profile", "email", "groups"],
    }

    print("\n✓ Access Token Claims:")
    for key, value in access_token_claims.items():
        print(f"  {key}: {value}")

    print("\n5. APPLICATION USER ASSIGNMENT")
    print("-" * 80)

    app_assignment = {
        "id": "app_assign_001",
        "app_id": "0oabcdefg123456",
        "user_id": "user001",
        "scope": ["openid", "profile", "email"],
        "role_assignments": ["role_engineer"],
        "profile": {
            "department": "Engineering",
            "cost_center": "12345",
        },
    }

    print("✓ Application Assignment:")
    print(f"  App ID: {app_assignment['app_id']}")
    print(f"  User ID: {app_assignment['user_id']}")
    print(f"  Scopes: {', '.join(app_assignment['scope'])}")
    print(f"  Roles: {', '.join(app_assignment['role_assignments'])}")

    print("\n6. SINGLE LOGOUT (SLO)")
    print("-" * 80)

    slo_flow = {
        "flow": "Single Logout Flow",
        "steps": [
            "1. User clicks 'Sign Out' on app",
            "2. App clears local session",
            "3. App redirects to Okta logout endpoint",
            "4. Okta clears Okta session",
            "5. Okta redirects to post-logout URI",
            "6. User logged out from all apps",
        ],
    }

    print("✓ OIDC Single Logout:")
    for step in slo_flow["steps"]:
        print(f"  {step}")

    print("\n7. API ENDPOINT EXAMPLES")
    print("-" * 80)

    endpoints = {
        "Authorization": "GET /oauth2/v1/authorize",
        "Token": "POST /oauth2/v1/token",
        "User Info": "GET /oauth2/v1/userinfo",
        "Logout": "POST /oauth2/v1/logout",
        "JWKS": "GET /oauth2/v1/keys",
        "Metadata": "GET /.well-known/openid-configuration",
    }

    print("✓ OAuth 2.0 / OIDC Endpoints:")
    for name, endpoint in endpoints.items():
        print(f"  {name}: {endpoint}")

    print("\n8. SECURITY BEST PRACTICES")
    print("-" * 80)

    best_practices = [
        "• Always use HTTPS for all endpoints",
        "• Validate token signatures using JWKS",
        "• Implement PKCE for mobile/SPA apps",
        "• Use state parameter to prevent CSRF",
        "• Store refresh tokens securely",
        "• Implement token rotation",
        "• Validate audience claim in tokens",
        "• Implement proper redirect URI validation",
        "• Monitor token usage for anomalies",
        "• Implement proper error handling",
    ]

    for practice in best_practices:
        print(f"  {practice}")

    print("\n" + "=" * 80)
    print("SSO & APPLICATION INTEGRATION EXAMPLE COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    example_sso_and_applications()
