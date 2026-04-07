"""
Okta API Client
Core client for interacting with Okta APIs
"""

import requests
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass
from enum import Enum


class AuthMethod(Enum):
    """Supported authentication methods"""
    OAUTH2 = "oauth2"
    SAML = "saml"
    API_TOKEN = "api_token"


@dataclass
class OktaConfig:
    """Okta configuration"""
    org_url: str
    api_token: str
    auth_method: AuthMethod = AuthMethod.API_TOKEN


class OktaClient:
    """
    Okta API Client for enterprise identity management
    Handles authentication, user management, and lifecycle operations
    """

    def __init__(self, config: OktaConfig):
        """
        Initialize Okta client

        Args:
            config: OktaConfig object with org URL and API token
        """
        self.config = config
        self.base_url = f"{config.org_url}/api/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_token}",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Okta API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(
                    url, headers=self.headers, json=data, params=params
                )
            elif method.upper() == "PUT":
                response = requests.put(
                    url, headers=self.headers, json=data, params=params
                )
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            if response.status_code == 204:
                return {"status": "success"}

            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Okta API error: {str(e)}")

    # ============== User Management ==============

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        login: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        activate: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a new user in Okta

        Args:
            email: User email
            first_name: First name
            last_name: Last name
            login: Login (defaults to email)
            mobile_phone: Mobile phone for MFA
            activate: Whether to activate immediately

        Returns:
            Created user object
        """
        login = login or email

        user_data = {
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "login": login,
                "mobilePhone": mobile_phone,
            }
        }

        params = {"activate": str(activate).lower()}
        return self._make_request("POST", "users", data=user_data, params=params)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID or login"""
        return self._make_request("GET", f"users/{user_id}")

    def list_users(self, query: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """List users with optional filter"""
        params = {"limit": limit}
        if query:
            params["search"] = query
        return self._make_request("GET", "users", params=params)

    def update_user(self, user_id: str, user_data: Dict) -> Dict[str, Any]:
        """Update user profile"""
        return self._make_request("PUT", f"users/{user_id}", data=user_data)

    def deactivate_user(self, user_id: str) -> Dict[str, Any]:
        """Deactivate user (identity lifecycle)"""
        return self._make_request("POST", f"users/{user_id}/lifecycle/deactivate")

    def reactivate_user(self, user_id: str) -> Dict[str, Any]:
        """Reactivate user"""
        return self._make_request("POST", f"users/{user_id}/lifecycle/reactivate")

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user permanently"""
        return self._make_request("DELETE", f"users/{user_id}")

    # ============== Group Management ==============

    def create_group(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a group"""
        group_data = {"profile": {"name": name, "description": description}}
        return self._make_request("POST", "groups", data=group_data)

    def list_groups(self, query: Optional[str] = None) -> List[Dict]:
        """List groups"""
        params = {}
        if query:
            params["q"] = query
        return self._make_request("GET", "groups", params=params)

    def add_user_to_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Add user to group (RBAC)"""
        return self._make_request(
            "PUT", f"groups/{group_id}/users/{user_id}", data={}
        )

    def remove_user_from_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Remove user from group"""
        return self._make_request("DELETE", f"groups/{group_id}/users/{user_id}")

    # ============== Authentication & MFA ==============

    def enable_factor(self, user_id: str, factor_type: str) -> Dict[str, Any]:
        """
        Enable MFA factor for user

        Args:
            user_id: User ID
            factor_type: Type of factor (OKTA, GOOGLE, DUO)

        Returns:
            Factor enrollment response
        """
        factor_data = {"factorType": factor_type, "provider": {"name": factor_type}}
        return self._make_request(
            "POST", f"users/{user_id}/factors", data=factor_data
        )

    def list_user_factors(self, user_id: str) -> List[Dict]:
        """List MFA factors for user"""
        return self._make_request("GET", f"users/{user_id}/factors")

    # ============== App Integration (SSO) ==============

    def create_app(
        self, name: str, label: str, app_type: str = "oidc"
    ) -> Dict[str, Any]:
        """
        Create OIDC application for SSO

        Args:
            name: App name
            label: Display label
            app_type: Application type (oidc, saml, etc)

        Returns:
            Created app object
        """
        app_data = {
            "name": name,
            "label": label,
            "signOnMode": "OPENID_CONNECT" if app_type == "oidc" else "SAML_2_0",
            "settings": {
                "oauthClient": {
                    "client_type": "public",
                    "redirect_uris": ["http://localhost:8080/callback"],
                    "response_types": ["code", "token"],
                    "grant_types": ["authorization_code", "refresh_token"],
                } if app_type == "oidc" else {}
            },
        }

        return self._make_request("POST", "apps", data=app_data)

    def list_apps(self) -> List[Dict]:
        """List all applications"""
        return self._make_request("GET", "apps")

    # ============== Policies (Zero Trust) ==============

    def create_access_policy(
        self, name: str, description: str, rules: List[Dict]
    ) -> Dict[str, Any]:
        """
        Create access control policy for zero trust

        Args:
            name: Policy name
            description: Policy description
            rules: List of policy rules with conditions

        Returns:
            Created policy object
        """
        policy_data = {
            "type": "ACCESS_POLICY",
            "name": name,
            "description": description,
            "rules": rules,
        }
        return self._make_request("POST", "policies", data=policy_data)

    def list_policies(self) -> List[Dict]:
        """List all policies"""
        return self._make_request("GET", "policies")

    # ============== SCIM Provisioning ==============

    def list_scim_resources(self) -> Dict[str, Any]:
        """List SCIM provisioning resources"""
        return self._make_request("GET", "scim/v2/Users")

    def create_scim_user(self, user_data: Dict) -> Dict[str, Any]:
        """Create user via SCIM"""
        return self._make_request("POST", "scim/v2/Users", data=user_data)
