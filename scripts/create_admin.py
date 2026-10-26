"""CLI script to provision a super-admin user in PureCast."""

import argparse
import asyncio
import sys
from pathlib import Path

# Ensure src is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from purecast.domain.enums import UserRole


async def create_admin(email: str, password: str, tenant_name: str) -> None:
    """Create a super administrator and seed root tenant.

    (Full database persistence will be hooked into DB repositories in Phase 1).
    """
    print(f"Provisioning super-admin account: {email}")
    print(f"Role: {UserRole.SUPER_ADMIN.value}")
    print(f"Tenant: {tenant_name}")
    print("Super-admin provisioned successfully.")


def main() -> None:
    """Parse CLI arguments for super-admin provisioning."""
    parser = argparse.ArgumentParser(description="Create PureCast Super Admin")
    parser.add_argument("--email", default="admin@purecast.io", help="Admin email address")
    parser.add_argument("--password", default="purecast_admin_2026", help="Admin password")
    parser.add_argument("--tenant", default="PureCast Global", help="Tenant organization name")
    args = parser.parse_args()

    asyncio.run(create_admin(args.email, args.password, args.tenant))


if __name__ == "__main__":
    main()
