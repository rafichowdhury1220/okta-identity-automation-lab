"""
Example menu for running different demonstrations
"""

import subprocess
import sys
from pathlib import Path


def print_menu():
    """Print example menu"""
    print("\n" + "=" * 80)
    print("OKTA IDENTITY AUTOMATION LAB - EXAMPLES")
    print("=" * 80)
    print("\nSelect an example to run:\n")
    print("1. Complete Identity Lifecycle")
    print("   Demonstrates: Onboarding, RBAC, MFA, Zero Trust, Offboarding")
    print()
    print("2. SCIM Provisioning & HR Integration")
    print("   Demonstrates: Bulk provisioning, Group management, Sync automation")
    print()
    print("3. SSO & Application Integration")
    print("   Demonstrates: OAuth 2.0/OIDC, SAML, SSO flows, Token management")
    print()
    print("4. Run All Examples")
    print()
    print("0. Exit")
    print()


def main_menu():
    """Main menu"""
    examples_dir = Path(__file__).parent
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-4): ").strip()

        if choice == "0":
            print("\nExiting...\n")
            break
        elif choice == "1":
            print("\n")
            subprocess.run([sys.executable, str(examples_dir / "01_complete_lifecycle.py")])
        elif choice == "2":
            print("\n")
            subprocess.run([sys.executable, str(examples_dir / "02_scim_provisioning.py")])
        elif choice == "3":
            print("\n")
            subprocess.run([sys.executable, str(examples_dir / "03_sso_applications.py")])
        elif choice == "4":
            print("\nRunning all examples...\n")
            subprocess.run([sys.executable, str(examples_dir / "01_complete_lifecycle.py")])
            print("\n\n")
            subprocess.run([sys.executable, str(examples_dir / "02_scim_provisioning.py")])
            print("\n\n")
            subprocess.run([sys.executable, str(examples_dir / "03_sso_applications.py")])
        else:
            print("\nInvalid choice. Please try again.\n")


if __name__ == "__main__":
    main_menu()
