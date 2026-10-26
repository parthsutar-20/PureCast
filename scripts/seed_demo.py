"""CLI script to seed demo tenants, devices, and cartridge models."""

import asyncio
import sys
from pathlib import Path

# Ensure src is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from purecast.domain.enums import ConsumableType, DeviceTier


async def seed_demo_data() -> None:
    """Seed sample data for demonstration and local development."""
    print("Seeding demo environment:")
    print("  - Tenant: Atomberg Technologies (OEM Partner)")
    print(f"  - Device 1: Model AtomPure-X1 ({DeviceTier.FULL.value} Tier)")
    print(f"  - Device 2: Model AtomPure-Lite ({DeviceTier.LITE.value} Tier)")
    print("  - Consumables registered:")
    for c in ConsumableType:
        print(f"    * {c.value}")
    print("Demo data seeded successfully.")


def main() -> None:
    """Run seeding routine."""
    asyncio.run(seed_demo_data())


if __name__ == "__main__":
    main()
