"""
Multi-Factor Authentication (MFA) Manager
Handles MFA configuration and enforcement
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class MFAFactorType(Enum):
    """Supported MFA factor types"""
    OKTA_VERIFY = "OKTA"
    GOOGLE_AUTHENTICATOR = "GOOGLE"
    DUO = "DUO"
    SMS = "SMS"
    EMAIL = "EMAIL"
    HARDWARE_TOKEN = "HARDWARE_TOKEN"


class MFAPolicy:
    """MFA Policy configuration"""

    def __init__(
        self,
        name: str,
        description: str,
        required_factors: List[MFAFactorType],
        exempted_groups: Optional[List[str]] = None,
    ):
        """
        Initialize MFA Policy

        Args:
            name: Policy name
            description: Policy description
            required_factors: List of required MFA factors
            exempted_groups: Groups exempt from MFA
        """
        self.name = name
        self.description = description
        self.required_factors = required_factors
        self.exempted_groups = exempted_groups or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert policy to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "required_factors": [factor.value for factor in self.required_factors],
            "exempted_groups": self.exempted_groups,
        }


class MFAManager:
    """
    Manages Multi-Factor Authentication
    Enforces MFA policies across organization
    """

    def __init__(self):
        """Initialize MFA Manager"""
        self.policies: Dict[str, MFAPolicy] = {}
        self.user_mfa_status: Dict[str, Dict[str, Any]] = {}

    def create_policy(
        self,
        policy_id: str,
        name: str,
        description: str,
        required_factors: List[MFAFactorType],
        exempted_groups: Optional[List[str]] = None,
    ) -> MFAPolicy:
        """
        Create MFA policy

        Args:
            policy_id: Unique policy identifier
            name: Policy name
            description: Policy description
            required_factors: List of required factors
            exempted_groups: Exempted groups

        Returns:
            Created MFAPolicy
        """
        policy = MFAPolicy(name, description, required_factors, exempted_groups)
        self.policies[policy_id] = policy
        return policy

    def get_policy(self, policy_id: str) -> Optional[MFAPolicy]:
        """Get MFA policy by ID"""
        return self.policies.get(policy_id)

    def list_policies(self) -> List[MFAPolicy]:
        """List all MFA policies"""
        return list(self.policies.values())

    def register_user_factor(
        self, user_id: str, factor_type: MFAFactorType, device_info: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Register MFA factor for user

        Args:
            user_id: User ID
            factor_type: Type of MFA factor
            device_info: Device information

        Returns:
            Factor registration status
        """
        if user_id not in self.user_mfa_status:
            self.user_mfa_status[user_id] = {
                "factors": [],
                "primary_factor": None,
                "enrolled": False,
            }

        factor = {
            "type": factor_type.value,
            "device_info": device_info,
            "enrolled_at": None,
            "verified": False,
        }

        self.user_mfa_status[user_id]["factors"].append(factor)

        if self.user_mfa_status[user_id]["primary_factor"] is None:
            self.user_mfa_status[user_id]["primary_factor"] = factor_type.value

        return {
            "status": "registered",
            "user_id": user_id,
            "factor": factor,
        }

    def verify_factor(
        self, user_id: str, factor_type: MFAFactorType, verification_code: str
    ) -> Dict[str, Any]:
        """
        Verify MFA factor

        Args:
            user_id: User ID
            factor_type: Factor type
            verification_code: Verification code

        Returns:
            Verification status
        """
        if user_id not in self.user_mfa_status:
            return {"status": "error", "message": "User not found"}

        factors = self.user_mfa_status[user_id]["factors"]
        for factor in factors:
            if factor["type"] == factor_type.value:
                # Simulate verification
                if len(verification_code) >= 6:
                    factor["verified"] = True
                    self.user_mfa_status[user_id]["enrolled"] = True
                    return {
                        "status": "verified",
                        "user_id": user_id,
                        "factor_type": factor_type.value,
                    }

        return {"status": "error", "message": "Factor not found or invalid code"}

    def get_user_mfa_status(self, user_id: str) -> Dict[str, Any]:
        """Get MFA status for user"""
        return self.user_mfa_status.get(
            user_id,
            {"status": "not_enrolled", "factors": []},
        )

    def is_mfa_enrolled(self, user_id: str) -> bool:
        """Check if user has MFA enrolled"""
        status = self.user_mfa_status.get(user_id, {})
        return status.get("enrolled", False)

    def enforce_mfa_for_group(self, group_id: str, policy_id: str) -> Dict[str, Any]:
        """
        Enforce MFA policy for a group

        Args:
            group_id: Group ID
            policy_id: MFA Policy ID

        Returns:
            Enforcement status
        """
        policy = self.get_policy(policy_id)
        if not policy:
            return {"status": "error", "message": "Policy not found"}

        return {
            "status": "enforced",
            "group_id": group_id,
            "policy": policy.to_dict(),
        }
