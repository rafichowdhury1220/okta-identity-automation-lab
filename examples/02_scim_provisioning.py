"""
Example: SCIM Provisioning and HR System Integration
Demonstrates bulk user provisioning and HR system synchronization
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scim_provisioning import SCIMProvisioningManager


def example_scim_provisioning():
    """SCIM provisioning example"""
    print("=" * 80)
    print("SCIM 2.0 PROVISIONING - HR SYSTEM INTEGRATION")
    print("=" * 80)

    scim_mgr = SCIMProvisioningManager()

    print("\n1. CREATE USERS VIA SCIM")
    print("-" * 80)

    # Create single user
    user1 = scim_mgr.create_user(
        user_id="user101",
        username="alice.smith@company.com",
        first_name="Alice",
        last_name="Smith",
        emails=["alice.smith@company.com", "asmith@company.com"],
        phone_numbers=["+1-555-0100", "+1-555-0101"],
    )
    print("✓ Created user (SCIM format):")
    print(f"  ID: {user1['id']}")
    print(f"  Username: {user1['userName']}")
    print(f"  Name: {user1['name']['givenName']} {user1['name']['familyName']}")
    print(f"  Emails: {len(user1['emails'])}")

    print("\n2. BATCH PROVISIONING FROM HR SYSTEM")
    print("-" * 80)

    # Simulate HR system export
    hr_users = [
        {
            "id": "user102",
            "userName": "bob.jones@company.com",
            "name": {
                "givenName": "Bob",
                "familyName": "Jones",
            },
            "emails": [
                {"value": "bob.jones@company.com", "primary": True},
                {"value": "bjones@company.com"},
            ],
            "active": True,
        },
        {
            "id": "user103",
            "userName": "carol.white@company.com",
            "name": {
                "givenName": "Carol",
                "familyName": "White",
            },
            "emails": [
                {"value": "carol.white@company.com", "primary": True},
            ],
            "active": True,
        },
        {
            "id": "user104",
            "userName": "david.brown@company.com",
            "name": {
                "givenName": "David",
                "familyName": "Brown",
            },
            "emails": [
                {"value": "david.brown@company.com", "primary": True},
            ],
            "active": True,
        },
    ]

    # Sync from HR
    sync_result = scim_mgr.sync_from_hr_system(hr_users)
    print(f"✓ Batch provisioning results:")
    print(f"  Total processed: {sync_result['total']}")
    print(f"  Created: {sync_result['created']}")
    print(f"  Updated: {sync_result['updated']}")
    print(f"  Failed: {sync_result['failed']}")

    print("\n3. LIST USERS (SCIM LIST ENDPOINT)")
    print("-" * 80)

    users_list = scim_mgr.list_users(start_index=1, count=10)
    print(f"✓ SCIM List Response:")
    print(f"  Total Results: {users_list['totalResults']}")
    print(f"  Items Per Page: {users_list['itemsPerPage']}")
    print(f"  Start Index: {users_list['startIndex']}")
    print(f"  Users returned: {len(users_list['Resources'])}")

    print(f"\n  Users:")
    for user in users_list["Resources"]:
        print(f"    - {user['name']['givenName']} {user['name']['familyName']} ({user['userName']})")

    print("\n4. CREATE SCIM GROUPS")
    print("-" * 80)

    # Create groups
    eng_group = scim_mgr.create_group(
        group_id="group_engineering",
        display_name="Engineering Team",
        member_ids=["user102", "user104"],
    )
    print(f"✓ Created group: {eng_group['displayName']}")
    print(f"  Members: {len(eng_group['members'])}")

    sales_group = scim_mgr.create_group(
        group_id="group_sales",
        display_name="Sales Team",
        member_ids=["user103"],
    )
    print(f"✓ Created group: {sales_group['displayName']}")
    print(f"  Members: {len(sales_group['members'])}")

    print("\n5. MANAGE GROUP MEMBERSHIP")
    print("-" * 80)

    # Add user to group
    add_result = scim_mgr.add_member_to_group("group_sales", "user102")
    print(f"✓ Added user102 to sales group")
    print(f"  Total members: {len(add_result['members'])}")

    # Remove user from group
    remove_result = scim_mgr.remove_member_from_group("group_engineering", "user104")
    print(f"✓ Removed user104 from engineering group")
    print(f"  Total members: {len(remove_result['members'])}")

    print("\n6. UPDATE USER (SCIM PATCH)")
    print("-" * 80)

    update_data = {
        "name": {
            "givenName": "Robert",
            "familyName": "Jones",
        },
        "active": True,
    }
    updated_user = scim_mgr.update_user("user102", update_data)
    print(f"✓ Updated user:")
    print(f"  New name: {updated_user['name']['givenName']} {updated_user['name']['familyName']}")
    print(f"  Active: {updated_user['active']}")

    print("\n7. SYNC LOG / AUDIT TRAIL")
    print("-" * 80)

    sync_log = scim_mgr.get_sync_log()
    print(f"✓ Sync operations logged: {len(sync_log)}")
    print(f"\n  Recent operations:")
    for log_entry in sync_log[-5:]:
        print(f"    - {log_entry['operation']}: {log_entry['timestamp']}")
        if log_entry['primary_id']:
            print(f"      ID: {log_entry['primary_id']}")

    print("\n8. SCIM SCHEMA")
    print("-" * 80)

    schema = scim_mgr.get_scim_schema()
    print(f"✓ SCIM Schema ID: {schema['id']}")
    print(f"  Name: {schema['name']}")
    print(f"  Attributes: {len(schema['attributes'])}")
    for attr in schema["attributes"]:
        print(f"    - {attr['name']} ({attr['type']})")

    print("\n9. BULK USER DEPROVISIONING")
    print("-" * 80)

    # Bulk delete/deactivate
    delete_result = scim_mgr.delete_user("user104")
    print(f"✓ Deleted user104: {delete_result['status']}")

    # Check updated user list
    final_users = scim_mgr.list_users()
    print(f"✓ Final user count: {final_users['totalResults']}")

    print("\n" + "=" * 80)
    print("SCIM PROVISIONING EXAMPLE COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    example_scim_provisioning()
