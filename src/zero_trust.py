"""
Zero Trust Authentication Framework
Implements zero trust principles: verify every access request
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import hashlib


class TrustLevel(Enum):
    """Trust levels for zero trust evaluation"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContextFactor:
    """Contextual factor for zero trust evaluation"""

    def __init__(self, name: str, weight: float = 1.0):
        """
        Initialize context factor

        Args:
            name: Factor name
            weight: Weight in trust calculation (0.0-1.0)
        """
        self.name = name
        self.weight = weight
        self.value = 0.0

    def evaluate(self) -> float:
        """Evaluate factor and return trust score"""
        return self.value * self.weight


class AccessRequest:
    """Access request for zero trust evaluation"""

    def __init__(
        self,
        request_id: str,
        user_id: str,
        resource: str,
        ip_address: str,
        device_id: str,
        timestamp: Optional[datetime] = None,
    ):
        """Initialize access request"""
        self.request_id = request_id
        self.user_id = user_id
        self.resource = resource
        self.ip_address = ip_address
        self.device_id = device_id
        self.timestamp = timestamp or datetime.now()
        self.context_factors: Dict[str, Any] = {}
        self.decision = None
        self.trust_score = 0.0


class ZeroTrustEngine:
    """
    Zero Trust Authentication Engine
    Never trust by default, always verify
    """

    def __init__(self):
        """Initialize zero trust engine"""
        self.policies: Dict[str, Dict[str, Any]] = {}
        self.trusted_devices: Dict[str, Dict[str, Any]] = {}
        self.trusted_networks: List[str] = []
        self.access_log: List[Dict[str, Any]] = []
        self.mfa_required_resources = {"admin_panel", "user_management", "settings"}

    def register_device(
        self, device_id: str, device_type: str, device_name: str, user_id: str
    ) -> Dict[str, Any]:
        """
        Register and trust a device

        Args:
            device_id: Device identifier
            device_type: Type of device (laptop, phone, etc)
            device_name: Device name
            user_id: User ID

        Returns:
            Registration status
        """
        self.trusted_devices[device_id] = {
            "device_type": device_type,
            "device_name": device_name,
            "user_id": user_id,
            "registered_at": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "risk_score": 0.0,
        }

        return {
            "status": "device_trusted",
            "device_id": device_id,
            "device_name": device_name,
        }

    def add_trusted_network(self, cidr_range: str, network_name: str) -> Dict[str, Any]:
        """
        Add trusted network (office IP range, etc)

        Args:
            cidr_range: CIDR notation network range
            network_name: Network name

        Returns:
            Add status
        """
        self.trusted_networks.append(cidr_range)

        return {
            "status": "network_trusted",
            "cidr_range": cidr_range,
            "network_name": network_name,
        }

    def evaluate_access(self, request: AccessRequest) -> Dict[str, Any]:
        """
        Evaluate access request using zero trust principles

        Args:
            request: AccessRequest object

        Returns:
            Access decision with trust score
        """
        decision = {
            "request_id": request.request_id,
            "user_id": request.user_id,
            "resource": request.resource,
            "timestamp": request.timestamp.isoformat(),
            "decision": "DENIED",
            "trust_score": 0.0,
            "factors": {},
            "required_actions": [],
        }

        # Factor 1: User Identity (10%)
        user_trust = self._evaluate_user_identity(request.user_id)
        decision["factors"]["user_identity"] = user_trust

        # Factor 2: Device Trust (20%)
        device_trust = self._evaluate_device_trust(request.device_id)
        decision["factors"]["device_trust"] = device_trust

        # Factor 3: Network Trust (15%)
        network_trust = self._evaluate_network_trust(request.ip_address)
        decision["factors"]["network_trust"] = network_trust

        # Factor 4: Resource Sensitivity (20%)
        resource_sensitivity = self._evaluate_resource_sensitivity(request.resource)
        decision["factors"]["resource_sensitivity"] = resource_sensitivity

        # Factor 5: Time-based Risk (10%)
        time_risk = self._evaluate_time_risk(request.timestamp)
        decision["factors"]["time_risk"] = time_risk

        # Factor 6: Behavior Analysis (25%)
        behavior_risk = self._evaluate_behavior_risk(request)
        decision["factors"]["behavior_risk"] = behavior_risk

        # Calculate overall trust score
        total_score = (
            user_trust * 0.10
            + device_trust * 0.20
            + network_trust * 0.15
            + (1.0 - resource_sensitivity) * 0.20
            + (1.0 - time_risk) * 0.10
            + (1.0 - behavior_risk) * 0.25
        )

        decision["trust_score"] = round(total_score, 3)

        # Make decision and determine required actions
        if decision["trust_score"] >= 0.8:
            decision["decision"] = "ALLOWED"
        elif decision["trust_score"] >= 0.5:
            decision["decision"] = "CONDITIONAL_ALLOW"
            decision["required_actions"].append("mfa_required")
        else:
            decision["decision"] = "DENIED"
            decision["required_actions"].append("manual_review_required")

        # Always require MFA for sensitive resources
        if resource_sensitivity > 0.7 and "mfa_required" not in decision["required_actions"]:
            decision["required_actions"].append("mfa_required")

        request.decision = decision["decision"]
        self._log_access(decision)

        return decision

    def _evaluate_user_identity(self, user_id: str) -> float:
        """Evaluate user identity trust (0.0-1.0)"""
        # In production: check user reputation, historical behavior, etc
        # For now: assume authenticated users have base trust
        return 0.7

    def _evaluate_device_trust(self, device_id: str) -> float:
        """Evaluate device trust score"""
        if device_id in self.trusted_devices:
            device = self.trusted_devices[device_id]
            # Device is registered and trusted
            risk = device.get("risk_score", 0.0)
            return max(0.0, 1.0 - risk)
        # Unregistered device: lower trust
        return 0.3

    def _evaluate_network_trust(self, ip_address: str) -> float:
        """Evaluate network trust based on IP address"""
        for network in self.trusted_networks:
            if self._is_ip_in_network(ip_address, network):
                return 0.9

        # Unknown network: medium trust
        return 0.4

    def _evaluate_resource_sensitivity(self, resource: str) -> float:
        """Evaluate resource sensitivity (0.0-1.0, higher = more sensitive)"""
        sensitive_resources = {
            "admin_panel": 0.95,
            "user_management": 0.9,
            "settings": 0.8,
            "reports": 0.6,
            "documents": 0.5,
        }
        return sensitive_resources.get(resource, 0.3)

    def _evaluate_time_risk(self, timestamp: datetime) -> float:
        """Evaluate time-based risk (0.0-1.0)"""
        hour = timestamp.hour
        # Higher risk during unusual hours
        if 9 <= hour <= 17:
            return 0.1  # Business hours: low risk
        elif 18 <= hour <= 22:
            return 0.3  # Evening: medium risk
        else:
            return 0.7  # Night: high risk

    def _evaluate_behavior_risk(self, request: AccessRequest) -> float:
        """Evaluate behavioral anomaly risk"""
        # Check for anomalies:
        # - Unusual resource access pattern
        # - Rapid resource access
        # - etc
        return 0.2  # Baseline low risk

    def _is_ip_in_network(self, ip: str, cidr: str) -> bool:
        """Check if IP is in CIDR network"""
        # Simplified check - in production use ipaddress module
        return ip.startswith(cidr.split("/")[0].rsplit(".", 1)[0])

    def _log_access(self, decision: Dict[str, Any]) -> None:
        """Log access decision for audit"""
        self.access_log.append(decision)

    def require_mfa_for_resource(self, resource: str) -> Dict[str, Any]:
        """Require MFA for resource access"""
        self.mfa_required_resources.add(resource)
        return {
            "status": "updated",
            "resource": resource,
            "mfa_required": True,
        }

    def is_mfa_required(self, resource: str) -> bool:
        """Check if MFA is required for resource"""
        return resource in self.mfa_required_resources

    def get_access_policy(self, resource: str) -> Dict[str, Any]:
        """Get access policy for resource"""
        return {
            "resource": resource,
            "mfa_required": self.is_mfa_required(resource),
            "minimum_trust_score": 0.5,
            "trusted_networks": self.trusted_networks,
        }

    def audit_access_log(
        self, user_id: Optional[str] = None, days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get access log"""
        log = self.access_log

        if user_id:
            log = [entry for entry in log if entry.get("user_id") == user_id]

        # Filter by date if needed
        return log[-100:]  # Return last 100 entries
