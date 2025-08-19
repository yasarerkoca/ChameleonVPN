"""Utility script to export the FastAPI OpenAPI schema."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DEFAULT_ENV = {
    "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
    "SECRET_KEY": "x" * 16,
    "SESSION_SECRET_KEY": "x" * 16,
}
for key, value in DEFAULT_ENV.items():
    os.environ.setdefault(key, value)

from app.main import app


async def export_openapi(output: Path) -> None:
    """Generate the OpenAPI schema and write it to ``output``."""
    await app.router.startup()
    schema = app.openapi()
    output.write_text(json.dumps(schema, indent=2))
    await app.router.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export FastAPI OpenAPI schema")
    parser.add_argument("path", type=Path, help="Destination file path")
    args = parser.parse_args()
    asyncio.run(export_openapi(args.path))


if __name__ == "__main__":
    main()

