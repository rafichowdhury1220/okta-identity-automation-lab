"""
Example: Complete Identity Lifecycle Automation
Demonstrates onboarding, lifecycle management, and offboarding
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.identity_lifecycle import IdentityLifecycleManager, UserStatus
from src.rbac_manager import RBACManager
from src.mfa_manager import MFAManager, MFAFactorType
from src.zero_trust import ZeroTrustEngine, AccessRequest
from datetime import datetime


def example_complete_lifecycle():
    """Complete identity lifecycle example"""
    print("=" * 80)
    print("OKTA IDENTITY LIFECYCLE AUTOMATION - COMPLETE EXAMPLE")
    print("=" * 80)

    # Initialize managers
    lifecycle_mgr = IdentityLifecycleManager()
    rbac_mgr = RBACManager()
    mfa_mgr = MFAManager()
    zero_trust = ZeroTrustEngine()

    print("\n1. EMPLOYEE ONBOARDING (Day 1)")
    print("-" * 80)

    # Create new employee
    new_user = lifecycle_mgr.create_user(
        user_id="user001",
        email="john.doe@company.com",
        first_name="John",
        last_name="Doe",
        department="Engineering",
        manager_id="mgr001",
    )
    print(f"✓ Created user: {new_user.first_name} {new_user.last_name}")
    print(f"  Email: {new_user.email}")
    print(f"  Status: {new_user.status.value}")

    # Provision resources
    provision_result = lifecycle_mgr.provision_user("user001")
    print(f"\n✓ Provisioned resources:")
    for resource, value in provision_result["resources_created"].items():
        print(f"  - {resource}: {value}")

    # Activate user
    activate_result = lifecycle_mgr.activate_user("user001")
    print(f"\n✓ User activated: {activate_result['can_access_applications']}")

    print("\n2. ROLE-BASED ACCESS CONTROL (RBAC) - ASSIGNMENT")
    print("-" * 80)

    # Create permissions
    rbac_mgr.create_permission(
        "perm001",
        "View Reports",
        "Can view all company reports",
        "reports",
        "read",
    )
    rbac_mgr.create_permission(
        "perm002",
        "Edit Documents",
        "Can edit shared documents",
        "documents",
        "write",
    )
    rbac_mgr.create_permission(
        "perm003",
        "Manage Users",
        "Can manage user accounts",
        "users",
        "write",
    )

    # Create roles
    engineer_role = rbac_mgr.create_role(
        "role_engineer",
        "Software Engineer",
        "Standard engineer role",
        ["perm001", "perm002"],
    )
    print(f"✓ Created role: {engineer_role.name}")
    print(f"  Permissions: {', '.join(engineer_role.permissions)}")

    admin_role = rbac_mgr.create_role(
        "role_admin",
        "System Administrator",
        "Admin role with elevated permissions",
        ["perm001", "perm002", "perm003"],
    )
    print(f"✓ Created role: {admin_role.name}")

    # Assign role to user
    assign_result = rbac_mgr.assign_role_to_user("user001", "role_engineer")
    print(f"\n✓ Assigned role to user: {assign_result['role_id']}")

    # Check user permissions
    user_perms = rbac_mgr.get_user_permissions("user001")
    print(f"✓ User permissions: {user_perms}")

    # Assign to group
    group_assign = lifecycle_mgr.assign_group("user001", "group_engineering")
    print(f"✓ Assigned to group: {group_assign['group_id']}")

    print("\n3. MULTI-FACTOR AUTHENTICATION (MFA) - ENROLLMENT")
    print("-" * 80)

    # Create MFA policy
    mfa_policy = mfa_mgr.create_policy(
        "policy_standard",
        "Standard MFA Policy",
        "MFA required for all users",
        [MFAFactorType.OKTA_VERIFY, MFAFactorType.SMS],
    )
    print(f"✓ Created MFA policy: {mfa_policy.name}")
    print(f"  Required factors: {[f.value for f in mfa_policy.required_factors]}")

    # Register MFA factor
    factor_result = mfa_mgr.register_user_factor(
        "user001",
        MFAFactorType.OKTA_VERIFY,
        {"device_name": "iPhone 14", "device_type": "mobile"},
    )
    print(f"\n✓ Registered MFA factor: {factor_result['factor']['type']}")
    print(f"  Device: {factor_result['factor']['device_info']['device_name']}")

    # Verify MFA factor (simulate verification)
    verify_result = mfa_mgr.verify_factor("user001", MFAFactorType.OKTA_VERIFY, "123456")
    print(f"✓ Verified MFA: {verify_result['status']}")

    mfa_status = mfa_mgr.get_user_mfa_status("user001")
    print(f"✓ MFA enrollment status: {mfa_status['enrolled']}")

    # Enforce policy for group
    enforce_result = mfa_mgr.enforce_mfa_for_group("group_engineering", "policy_standard")
    print(f"✓ Enforced MFA policy for group: {enforce_result['group_id']}")

    print("\n4. ZERO TRUST AUTHENTICATION")
    print("-" * 80)

    # Register device
    device_result = zero_trust.register_device(
        "device001",
        "laptop",
        "MacBook Pro",
        "user001",
    )
    print(f"✓ Registered device: {device_result['device_name']}")

    # Add trusted network
    network_result = zero_trust.add_trusted_network(
        "10.0.0.0/8",
        "Corporate Network",
    )
    print(f"✓ Added trusted network: {network_result['network_name']}")

    # Require MFA for admin resources
    zero_trust.require_mfa_for_resource("admin_panel")
    print(f"✓ MFA required for: admin_panel")

    # Evaluate access request to documents (low sensitivity)
    print("\n  Evaluating access to 'documents' (low sensitivity)...")
    access_request = AccessRequest(
        "req001",
        "user001",
        "documents",
        "10.0.0.100",
        "device001",
    )
    decision = zero_trust.evaluate_access(access_request)
    print(f"  Decision: {decision['decision']}")
    print(f"  Trust Score: {decision['trust_score']}")
    print(f"  Factors:")
    for factor, value in decision["factors"].items():
        print(f"    - {factor}: {value:.2f}")

    # Evaluate access request to admin panel (high sensitivity)
    print("\n  Evaluating access to 'admin_panel' (high sensitivity)...")
    admin_request = AccessRequest(
        "req002",
        "user001",
        "admin_panel",
        "203.0.113.50",  # Unknown external IP
        "unknown_device",
    )
    admin_decision = zero_trust.evaluate_access(admin_request)
    print(f"  Decision: {admin_decision['decision']}")
    print(f"  Trust Score: {admin_decision['trust_score']}")
    print(f"  Required Actions: {admin_decision['required_actions']}")

    print("\n5. USER STATUS AND AUDIT")
    print("-" * 80)

    user_status = lifecycle_mgr.get_user_status("user001")
    print(f"✓ User Status:")
    print(f"  ID: {user_status['id']}")
    print(f"  Email: {user_status['email']}")
    print(f"  Status: {user_status['status']}")
    print(f"  Roles: {user_status['roles']}")
    print(f"  Groups: {user_status['groups']}")

    # RBAC audit
    rbac_audit = rbac_mgr.audit_user_access("user001")
    print(f"\n✓ Access Audit:")
    print(f"  Roles: {rbac_audit['role_count']}")
    print(f"  Permissions: {rbac_audit['permission_count']}")
    print(f"  Resource Access:")
    print(f"    - Can view reports: {rbac_mgr.has_resource_access('user001', 'reports', 'read')}")
    print(f"    - Can edit documents: {rbac_mgr.has_resource_access('user001', 'documents', 'write')}")
    print(f"    - Can manage users: {rbac_mgr.has_resource_access('user001', 'users', 'write')}")

    print("\n6. EMPLOYEE OFFBOARDING (Day 1000)")
    print("-" * 80)

    # Suspend user
    suspend_result = lifecycle_mgr.suspend_user("user001", "Administrative leave")
    print(f"✓ User suspended: {not suspend_result['can_access']}")

    # Reactivate for example
    reactivate_result = lifecycle_mgr.reactivate_user("user001")
    print(f"✓ User reactivated: {reactivate_result['status']}")

    # Deprovision user
    deprovision_result = lifecycle_mgr.deprovision_user(
        "user001",
        effective_date="2024-03-15",
    )
    print(f"\n✓ User deprovisioned:")
    print(f"  Email access revoked: {deprovision_result['revoked']['email_access']}")
    print(f"  Application access revoked: {deprovision_result['revoked']['application_access']}")
    print(f"  VPN access revoked: {deprovision_result['revoked']['vpn_access']}")
    print(f"  Groups removed: {deprovision_result['revoked']['group_memberships']}")

    # Get lifecycle audit log
    audit_log = lifecycle_mgr.get_audit_log("user001")
    print(f"\n✓ Audit Log ({len(audit_log)} events):")
    for event in audit_log[-3:]:  # Show last 3 events
        print(f"  - {event['event']}: {event['timestamp']}")

    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    example_complete_lifecycle()
