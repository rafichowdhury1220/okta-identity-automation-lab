"""
Okta Identity Automation Lab - Main Entry Point
Demonstrates enterprise identity management capabilities
"""

import sys
from examples.example_menu import main_menu


def main():
    """Main entry point"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║            Okta Identity Automation Lab - Enterprise Identity Demo           ║")
    print("║                                                                              ║")
    print("║  Demonstrates enterprise identity architecture:                             ║")
    print("║  • Single Sign-On (SSO)                                                      ║")
    print("║  • Multi-Factor Authentication (MFA)                                         ║")
    print("║  • SCIM Provisioning                                                         ║")
    print("║  • Identity Lifecycle Automation                                             ║")
    print("║  • Role-Based Access Control (RBAC)                                          ║")
    print("║  • Zero Trust Authentication                                                 ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")

    main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}\n")
        sys.exit(1)
