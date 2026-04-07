"""
SCIM 2.0 Provisioning Manager
Handles System for Cross-domain Identity Management provisioning
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SCIMUser:
    """SCIM 2.0 User representation"""
    id: str
    user_name: str
    name_given: str
    name_family: str
    emails: List[Dict[str, str]]
    phone_numbers: Optional[List[Dict[str, str]]] = None
    active: bool = True
    meta: Optional[Dict[str, str]] = None

    def to_scim_json(self) -> Dict[str, Any]:
        """Convert to SCIM 2.0 JSON representation"""
        return {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": self.id,
            "userName": self.user_name,
            "name": {
                "givenName": self.name_given,
                "familyName": self.name_family,
            },
            "emails": self.emails,
            "phoneNumbers": self.phone_numbers or [],
            "active": self.active,
            "meta": self.meta or {
                "resourceType": "User",
                "created": datetime.now().isoformat(),
                "lastModified": datetime.now().isoformat(),
            },
        }


@dataclass
class SCIMGroup:
    """SCIM 2.0 Group representation"""
    id: str
    display_name: str
    members: List[str]
    description: Optional[str] = None

    def to_scim_json(self) -> Dict[str, Any]:
        """Convert to SCIM 2.0 JSON representation"""
        return {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
            "id": self.id,
            "displayName": self.display_name,
            "description": self.description,
            "members": [{"value": member_id} for member_id in self.members],
            "meta": {
                "resourceType": "Group",
                "created": datetime.now().isoformat(),
                "lastModified": datetime.now().isoformat(),
            },
        }


class SCIMProvisioningManager:
    """
    SCIM 2.0 Provisioning Manager
    Enables enterprise provisioning via SCIM protocol
    Synchronizes users and groups across systems
    """

    def __init__(self):
        """Initialize SCIM provisioning manager"""
        self.users: Dict[str, SCIMUser] = {}
        self.groups: Dict[str, SCIMGroup] = {}
        self.sync_log: List[Dict[str, Any]] = []
        self.batch_operations: List[Dict[str, Any]] = []

    def create_user(
        self,
        user_id: str,
        username: str,
        first_name: str,
        last_name: str,
        emails: List[str],
        phone_numbers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create user via SCIM

        Args:
            user_id: User ID
            username: Username
            first_name: First name
            last_name: Last name
            emails: List of email addresses
            phone_numbers: List of phone numbers

        Returns:
            Created user in SCIM format
        """
        email_list = [{"value": email, "primary": i == 0} for i, email in enumerate(emails)]
        phone_list = (
            [{"value": phone, "primary": i == 0} for i, phone in enumerate(phone_numbers)]
            if phone_numbers
            else []
        )

        user = SCIMUser(
            id=user_id,
            user_name=username,
            name_given=first_name,
            name_family=last_name,
            emails=email_list,
            phone_numbers=phone_list,
        )

        self.users[user_id] = user
        self._log_sync("user_created", user_id)

        return user.to_scim_json()

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user in SCIM format"""
        if user_id in self.users:
            return self.users[user_id].to_scim_json()
        return None

    def list_users(self, start_index: int = 1, count: int = 20) -> Dict[str, Any]:
        """
        List users (SCIM list endpoint)

        Args:
            start_index: Start index for pagination
            count: Number of results

        Returns:
            SCIM list response
        """
        users_list = list(self.users.values())[start_index - 1 : start_index - 1 + count]

        return {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": len(self.users),
            "startIndex": start_index,
            "itemsPerPage": len(users_list),
            "Resources": [user.to_scim_json() for user in users_list],
        }

    def update_user(
        self, user_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user (SCIM PATCH)

        Args:
            user_id: User ID
            updates: Fields to update

        Returns:
            Updated user
        """
        if user_id not in self.users:
            return {"error": "User not found"}

        user = self.users[user_id]

        if "name" in updates:
            if "givenName" in updates["name"]:
                user.name_given = updates["name"]["givenName"]
            if "familyName" in updates["name"]:
                user.name_family = updates["name"]["familyName"]

        if "active" in updates:
            user.active = updates["active"]

        self._log_sync("user_updated", user_id)
        return user.to_scim_json()

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user"""
        if user_id not in self.users:
            return {"error": "User not found"}

        del self.users[user_id]
        self._log_sync("user_deleted", user_id)

        return {"status": "deleted"}

    def create_group(
        self, group_id: str, display_name: str, member_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create group via SCIM

        Args:
            group_id: Group ID
            display_name: Display name
            member_ids: List of member user IDs

        Returns:
            Created group in SCIM format
        """
        group = SCIMGroup(
            id=group_id,
            display_name=display_name,
            members=member_ids or [],
        )

        self.groups[group_id] = group
        self._log_sync("group_created", group_id)

        return group.to_scim_json()

    def add_member_to_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Add member to group"""
        if group_id not in self.groups:
            return {"error": "Group not found"}

        group = self.groups[group_id]
        if user_id not in group.members:
            group.members.append(user_id)
            self._log_sync("user_added_to_group", group_id, user_id)

        return group.to_scim_json()

    def remove_member_from_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Remove member from group"""
        if group_id not in self.groups:
            return {"error": "Group not found"}

        group = self.groups[group_id]
        if user_id in group.members:
            group.members.remove(user_id)
            self._log_sync("user_removed_from_group", group_id, user_id)

        return group.to_scim_json()

    def batch_upsert_users(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Batch upsert users (bulk provisioning)

        Args:
            users: List of user data

        Returns:
            Batch operation status
        """
        results = {
            "total": len(users),
            "created": 0,
            "updated": 0,
            "failed": 0,
        }

        for user_data in users:
            try:
                user_id = user_data.get("id")
                if user_id in self.users:
                    self.update_user(user_id, user_data)
                    results["updated"] += 1
                else:
                    self.create_user(
                        user_id,
                        user_data.get("userName"),
                        user_data["name"].get("givenName"),
                        user_data["name"].get("familyName"),
                        [email["value"] for email in user_data.get("emails", [])],
                    )
                    results["created"] += 1
            except Exception:
                results["failed"] += 1

        self._log_sync("batch_upsert", None, None, results)
        return results

    def sync_from_hr_system(self, hr_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync users from HR system (lifecycle automation)

        Args:
            hr_users: Users from HR system

        Returns:
            Sync results
        """
        return self.batch_upsert_users(hr_users)

    def get_sync_log(self) -> List[Dict[str, Any]]:
        """Get synchronization audit log"""
        return self.sync_log

    def _log_sync(
        self,
        operation: str,
        primary_id: Optional[str] = None,
        secondary_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log sync operation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "primary_id": primary_id,
            "secondary_id": secondary_id,
            "details": details or {},
        }
        self.sync_log.append(log_entry)

    def get_scim_schema(self) -> Dict[str, Any]:
        """Return SCIM schema definition"""
        return {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:Schema",
            ],
            "id": "urn:ietf:params:scim:schemas:core:2.0:User",
            "name": "User",
            "description": "SCIM 2.0 User resource",
            "attributes": [
                {
                    "name": "userName",
                    "type": "string",
                    "required": True,
                    "caseExact": False,
                },
                {
                    "name": "name",
                    "type": "complex",
                    "subAttributes": [
                        {"name": "givenName", "type": "string"},
                        {"name": "familyName", "type": "string"},
                    ],
                },
                {
                    "name": "emails",
                    "type": "complex",
                    "multiValued": True,
                    "subAttributes": [
                        {"name": "value", "type": "string"},
                        {"name": "primary", "type": "boolean"},
                    ],
                },
                {
                    "name": "active",
                    "type": "boolean",
                    "default": True,
                },
            ],
        }
