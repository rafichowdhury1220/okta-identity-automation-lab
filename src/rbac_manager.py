"""
Role-Based Access Control (RBAC) Manager
Manages user roles, permissions, and access controls
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Permission:
    """Permission definition"""
    id: str
    name: str
    description: str
    resource: str
    action: str


@dataclass
class Role:
    """Role definition"""
    id: str
    name: str
    description: str
    permissions: Set[str] = field(default_factory=set)
    parent_roles: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": list(self.permissions),
            "parent_roles": self.parent_roles,
        }


class RBACManager:
    """
    Role-Based Access Control Manager
    Manages enterprise roles, permissions, and access policies
    """

    def __init__(self):
        """Initialize RBAC manager"""
        self.roles: Dict[str, Role] = {}
        self.permissions: Dict[str, Permission] = {}
        self.user_roles: Dict[str, Set[str]] = {}  # user_id -> roles
        self.user_permissions: Dict[str, Set[str]] = {}  # user_id -> permissions

    def create_permission(
        self,
        permission_id: str,
        name: str,
        description: str,
        resource: str,
        action: str,
    ) -> Permission:
        """
        Create a permission

        Args:
            permission_id: Permission ID
            name: Permission name
            description: Permission description
            resource: Resource name (e.g., 'app', 'users', 'reports')
            action: Action (e.g., 'read', 'write', 'delete')

        Returns:
            Created Permission
        """
        permission = Permission(permission_id, name, description, resource, action)
        self.permissions[permission_id] = permission
        return permission

    def create_role(
        self,
        role_id: str,
        name: str,
        description: str,
        permissions: Optional[List[str]] = None,
    ) -> Role:
        """
        Create a role

        Args:
            role_id: Role ID
            name: Role name
            description: Role description
            permissions: List of permission IDs

        Returns:
            Created Role
        """
        role = Role(
            role_id,
            name,
            description,
            set(permissions or []),
        )
        self.roles[role_id] = role
        return role

    def assign_role_to_user(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """
        Assign role to user

        Args:
            user_id: User ID
            role_id: Role ID

        Returns:
            Assignment status
        """
        if role_id not in self.roles:
            return {"status": "error", "message": "Role not found"}

        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()

        self.user_roles[user_id].add(role_id)
        self._update_user_permissions(user_id)

        return {
            "status": "assigned",
            "user_id": user_id,
            "role_id": role_id,
            "roles": list(self.user_roles[user_id]),
        }

    def remove_role_from_user(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """Remove role from user"""
        if user_id not in self.user_roles or role_id not in self.user_roles[user_id]:
            return {"status": "error", "message": "User-role assignment not found"}

        self.user_roles[user_id].discard(role_id)
        self._update_user_permissions(user_id)

        return {
            "status": "removed",
            "user_id": user_id,
            "role_id": role_id,
            "roles": list(self.user_roles[user_id]),
        }

    def add_permission_to_role(self, role_id: str, permission_id: str) -> Dict[str, Any]:
        """Add permission to role"""
        if role_id not in self.roles:
            return {"status": "error", "message": "Role not found"}

        if permission_id not in self.permissions:
            return {"status": "error", "message": "Permission not found"}

        self.roles[role_id].permissions.add(permission_id)

        # Update all users with this role
        for user_id, user_role_ids in self.user_roles.items():
            if role_id in user_role_ids:
                self._update_user_permissions(user_id)

        return {
            "status": "added",
            "role_id": role_id,
            "permission_id": permission_id,
        }

    def get_user_roles(self, user_id: str) -> List[str]:
        """Get roles for user"""
        return list(self.user_roles.get(user_id, set()))

    def get_user_permissions(self, user_id: str) -> List[str]:
        """Get permissions for user"""
        return list(self.user_permissions.get(user_id, set()))

    def has_permission(self, user_id: str, permission_id: str) -> bool:
        """Check if user has permission"""
        return permission_id in self.user_permissions.get(user_id, set())

    def has_resource_access(self, user_id: str, resource: str, action: str) -> bool:
        """
        Check if user can perform action on resource

        Args:
            user_id: User ID
            resource: Resource name
            action: Action name

        Returns:
            True if user has access
        """
        user_permissions = self.user_permissions.get(user_id, set())
        for perm_id in user_permissions:
            if perm_id in self.permissions:
                perm = self.permissions[perm_id]
                if perm.resource == resource and perm.action == action:
                    return True
        return False

    def set_role_hierarchy(self, role_id: str, parent_roles: List[str]) -> Dict[str, Any]:
        """
        Set parent roles (role hierarchy)

        Args:
            role_id: Role ID
            parent_roles: List of parent role IDs

        Returns:
            Update status
        """
        if role_id not in self.roles:
            return {"status": "error", "message": "Role not found"}

        self.roles[role_id].parent_roles = parent_roles

        # Recompute permissions for all users
        for user_id in self.user_roles:
            self._update_user_permissions(user_id)

        return {
            "status": "updated",
            "role_id": role_id,
            "parent_roles": parent_roles,
        }

    def _update_user_permissions(self, user_id: str) -> None:
        """
        Update user's effective permissions based on assigned roles
        Resolves role hierarchy
        """
        if user_id not in self.user_roles:
            return

        permissions = set()
        visited_roles = set()

        def collect_permissions(role_id: str) -> None:
            if role_id in visited_roles:
                return
            visited_roles.add(role_id)

            if role_id in self.roles:
                role = self.roles[role_id]
                permissions.update(role.permissions)

                # Add permissions from parent roles
                for parent_id in role.parent_roles:
                    collect_permissions(parent_id)

        for role_id in self.user_roles[user_id]:
            collect_permissions(role_id)

        self.user_permissions[user_id] = permissions

    def get_role_details(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed role information"""
        if role_id not in self.roles:
            return None

        role = self.roles[role_id]
        role_dict = role.to_dict()

        # Include permission details
        role_dict["permission_details"] = [
            self.permissions[perm_id].to_dict()
            if perm_id in self.permissions else {}
            for perm_id in role.permissions
        ]

        return role_dict

    def list_roles(self) -> List[Dict[str, Any]]:
        """List all roles"""
        return [role.to_dict() for role in self.roles.values()]

    def audit_user_access(self, user_id: str) -> Dict[str, Any]:
        """
        Audit user access and permissions

        Args:
            user_id: User ID

        Returns:
            Access audit report
        """
        return {
            "user_id": user_id,
            "roles": self.get_user_roles(user_id),
            "permissions": self.get_user_permissions(user_id),
            "permission_count": len(self.user_permissions.get(user_id, set())),
            "role_count": len(self.user_roles.get(user_id, set())),
        }
