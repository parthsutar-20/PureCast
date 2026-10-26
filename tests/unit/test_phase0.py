"""Phase 0 scaffold verification tests.

Validates that:
1. All domain enumerations contain expected values and inherit properly.
2. Physics and domain constants have valid numerical ranges and defaults.
3. The FastAPI application initializes cleanly and health/readiness endpoints respond.
4. Database declarative base initializes with proper metadata naming conventions.
"""

from enum import StrEnum

import pytest
from starlette.testclient import TestClient

from purecast import __version__
from purecast.core.constants import (
    AGEING_MULTIPLIER_RO,
    AGEING_MULTIPLIER_UF_UV,
    AGEING_MULTIPLIER_VACAY,
    EOL_FLOW_DROP_FRACTION,
    EOL_PREFILTER_DP_RISE_FRACTION,
    EOL_SALT_PASSAGE_RISE_FRACTION,
    REFERENCE_TEMPERATURE_C,
    TEMPERATURE_COEFFICIENT,
)
from purecast.domain.enums import (
    AlertSeverity,
    AlertStatus,
    ConsumableType,
    DeviceTier,
    EventType,
    FaultType,
    OperatingMode,
    OrderStatus,
    PlanTier,
    SensorFaultType,
    ServiceRequestStatus,
    UserRole,
)
from purecast.infrastructure.db.models import Base
from purecast.main import app


@pytest.mark.unit
def test_version_defined() -> None:
    """Ensure the package version is defined and follows semver."""
    assert __version__ == "0.1.0"


@pytest.mark.unit
def test_domain_enums_are_str_enums() -> None:
    """Ensure domain enums inherit from StrEnum for JSON serialization."""
    enums = [
        ConsumableType,
        FaultType,
        OperatingMode,
        DeviceTier,
        UserRole,
        AlertSeverity,
        AlertStatus,
        SensorFaultType,
        EventType,
        PlanTier,
        OrderStatus,
        ServiceRequestStatus,
    ]
    for enum_cls in enums:
        assert issubclass(enum_cls, StrEnum), f"{enum_cls} must inherit from StrEnum"


@pytest.mark.unit
def test_consumable_types() -> None:
    """Validate all 5 purifier consumables are enumerated."""
    expected = {"SEDIMENT", "CARBON", "MEMBRANE_PROTECTOR", "RO_MEMBRANE", "UV_LAMP"}
    actual = {c.value for c in ConsumableType}
    assert actual == expected


@pytest.mark.unit
def test_fault_types() -> None:
    """Validate all 5 purifier fault types are enumerated."""
    expected = {
        "PREFILTER_CLOG",
        "MEMBRANE_FOULING_SCALING",
        "MEMBRANE_WEAR",
        "SUPPLY_FAULT",
        "UV_LAMP_WEAKENING",
    }
    actual = {f.value for f in FaultType}
    assert actual == expected


@pytest.mark.unit
def test_constants_physics_validity() -> None:
    """Validate physical plausibility of domain constants."""
    assert 0.02 <= TEMPERATURE_COEFFICIENT <= 0.03
    assert REFERENCE_TEMPERATURE_C == 25.0
    assert 0.05 <= EOL_FLOW_DROP_FRACTION <= 0.20
    assert 0.05 <= EOL_SALT_PASSAGE_RISE_FRACTION <= 0.15
    assert 0.10 <= EOL_PREFILTER_DP_RISE_FRACTION <= 0.20
    assert AGEING_MULTIPLIER_RO > AGEING_MULTIPLIER_UF_UV > AGEING_MULTIPLIER_VACAY > 0.0


@pytest.mark.unit
def test_db_base_metadata_naming_convention() -> None:
    """Validate SQLAlchemy Base metadata naming convention is configured."""
    convention = Base.metadata.naming_convention
    assert "pk" in convention
    assert "fk" in convention
    assert "ix" in convention
    assert "uq" in convention


@pytest.mark.unit
def test_api_health_endpoints() -> None:
    """Validate FastAPI health and readiness endpoints."""
    with TestClient(app) as client:
        # Liveness
        res_health = client.get("/health")
        assert res_health.status_code == 200
        assert res_health.json() == {"status": "healthy"}

        # Readiness
        res_ready = client.get("/ready")
        assert res_ready.status_code == 200
        assert res_ready.json() == {"status": "ready"}

        # Root
        res_root = client.get("/")
        assert res_root.status_code == 200
        data = res_root.json()
        assert data["service"] == "PureCast API"
        assert data["version"] == __version__
