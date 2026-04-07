"""
Identity Lifecycle Management
Manages user onboarding, offboarding, and state transitions
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class UserStatus(Enum):
    """User lifecycle status"""
    ACTIVE = "ACTIVE"
    STAGING = "STAGING"
    PROVISIONED = "PROVISIONED"
    PRE_ACTIVATION = "PRE_ACTIVATION"
    DEPROVISIONED = "DEPROVISIONED"
    SUSPENDED = "SUSPENDED"


class LifecycleEvent(Enum):
    """Lifecycle events"""
    CREATED = "USER_CREATED"
    ACTIVATED = "USER_ACTIVATED"
    PROVISIONED = "USER_PROVISIONED"
    DEPROVISIONED = "USER_DEPROVISIONED"
    SUSPENDED = "USER_SUSPENDED"
    REACTIVATED = "USER_REACTIVATED"
    DELETED = "USER_DELETED"


class UserProfile:
    """User profile with lifecycle state"""

    def __init__(
        self,
        user_id: str,
        email: str,
        first_name: str,
        last_name: str,
        department: str,
        manager_id: Optional[str] = None,
    ):
        """Initialize user profile"""
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.manager_id = manager_id
        self.status = UserStatus.STAGING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.lifecycle_events: List[Dict[str, Any]] = []
        self.roles: List[str] = []
        self.groups: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.user_id,
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "department": self.department,
            "managerId": self.manager_id,
            "status": self.status.value,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "roles": self.roles,
            "groups": self.groups,
        }


class IdentityLifecycleManager:
    """
    Manages identity lifecycle: provisioning, activation, deprovisioning
    Handles onboarding and offboarding workflows
    """

    def __init__(self):
        """Initialize lifecycle manager"""
        self.users: Dict[str, UserProfile] = {}
        self.lifecycle_rules: Dict[str, Any] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def create_user(
        self,
        user_id: str,
        email: str,
        first_name: str,
        last_name: str,
        department: str,
        manager_id: Optional[str] = None,
    ) -> UserProfile:
        """
        Create new user (onboarding starts)

        Args:
            user_id: Unique user ID
            email: User email
            first_name: First name
            last_name: Last name
            department: Department
            manager_id: Manager ID

        Returns:
            Created UserProfile
        """
        user = UserProfile(
            user_id, email, first_name, last_name, department, manager_id
        )
        self.users[user_id] = user
        self._log_event(user_id, LifecycleEvent.CREATED)
        return user

    def provision_user(self, user_id: str) -> Dict[str, Any]:
        """
        Provision user (assign resources, create accounts)

        Args:
            user_id: User ID

        Returns:
            Provisioning status
        """
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        user.status = UserStatus.PROVISIONED
        user.updated_at = datetime.now()
        self._log_event(user_id, LifecycleEvent.PROVISIONED)

        return {
            "status": "provisioned",
            "user_id": user_id,
            "resources_created": {
                "email_account": f"{user.email}@organization.okta.com",
                "company_account": f"acc_{user_id}",
                "home_directory": f"/home/{user.email.split('@')[0]}",
                "vpn_access": True,
            },
        }

    def activate_user(self, user_id: str) -> Dict[str, Any]:
        """
        Activate user (make account fully functional)

        Args:
            user_id: User ID

        Returns:
            Activation status
        """
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        user.status = UserStatus.ACTIVE
        user.updated_at = datetime.now()
        self._log_event(user_id, LifecycleEvent.ACTIVATED)

        return {
            "status": "activated",
            "user_id": user_id,
            "can_access_applications": True,
        }

    def assign_role(self, user_id: str, role: str) -> Dict[str, Any]:
        """Assign role to user (RBAC)"""
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        if role not in user.roles:
            user.roles.append(role)
            user.updated_at = datetime.now()

        return {
            "status": "role_assigned",
            "user_id": user_id,
            "role": role,
            "roles": user.roles,
        }

    def assign_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Assign user to group (RBAC)"""
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        if group_id not in user.groups:
            user.groups.append(group_id)
            user.updated_at = datetime.now()

        return {
            "status": "group_assigned",
            "user_id": user_id,
            "group_id": group_id,
            "groups": user.groups,
        }

    def suspend_user(self, user_id: str, reason: str = "") -> Dict[str, Any]:
        """
        Suspend user access (e.g., administrative leave)

        Args:
            user_id: User ID
            reason: Suspension reason

        Returns:
            Suspension status
        """
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        user.status = UserStatus.SUSPENDED
        user.updated_at = datetime.now()
        self._log_event(user_id, LifecycleEvent.SUSPENDED, {"reason": reason})

        return {
            "status": "suspended",
            "user_id": user_id,
            "can_access": False,
        }

    def reactivate_user(self, user_id: str) -> Dict[str, Any]:
        """Reactivate suspended user"""
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        user.status = UserStatus.ACTIVE
        user.updated_at = datetime.now()
        self._log_event(user_id, LifecycleEvent.REACTIVATED)

        return {"status": "reactivated", "user_id": user_id}

    def deprovision_user(self, user_id: str, effective_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Deprovision user (offboarding - revoke access)

        Args:
            user_id: User ID
            effective_date: Offboarding effective date

        Returns:
            Deprovisioning status
        """
        user = self.users.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        user.status = UserStatus.DEPROVISIONED
        user.updated_at = datetime.now()
        user.roles.clear()
        user.groups.clear()
        self._log_event(user_id, LifecycleEvent.DEPROVISIONED)

        return {
            "status": "deprovisioned",
            "user_id": user_id,
            "revoked": {
                "email_access": True,
                "application_access": True,
                "vpn_access": True,
                "group_memberships": 0,
                "roles": [],
            },
            "effective_date": effective_date or "immediate",
        }

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        Permanently delete user

        Args:
            user_id: User ID

        Returns:
            Deletion status
        """
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}

        self._log_event(user_id, LifecycleEvent.DELETED)
        del self.users[user_id]

        return {"status": "deleted", "user_id": user_id}

    def get_user_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user lifecycle status"""
        user = self.users.get(user_id)
        if not user:
            return None
        return user.to_dict()

    def list_users_by_status(self, status: UserStatus) -> List[Dict[str, Any]]:
        """List users by lifecycle status"""
        return [
            user.to_dict()
            for user in self.users.values()
            if user.status == status
        ]

    def _log_event(
        self,
        user_id: str,
        event: LifecycleEvent,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log lifecycle event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "event": event.value,
            "details": details or {},
        }
        self.audit_log.append(log_entry)
        user = self.users.get(user_id)
        if user:
            user.lifecycle_events.append(log_entry)

    def get_audit_log(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get audit log"""
        if user_id:
            user = self.users.get(user_id)
            return user.lifecycle_events if user else []
        return self.audit_log
