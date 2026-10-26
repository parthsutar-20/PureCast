"""Export OpenAPI JSON specification from the FastAPI application."""

import json
import sys
from pathlib import Path

# Ensure src is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from purecast.main import app


def export_openapi() -> None:
    """Extract and write OpenAPI schema to docs/openapi.json."""
    output_path = Path(__file__).resolve().parent.parent / "docs" / "openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    openapi_data = app.openapi()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, indent=2)

    print(f"OpenAPI schema successfully written to {output_path}")


if __name__ == "__main__":
    export_openapi()
