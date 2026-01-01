import json
import pathlib

import pytest

json5 = pytest.importorskip("json5")
jsonschema = pytest.importorskip("jsonschema")


def repo_root() -> pathlib.Path:
    # ai/tests -> ai -> <repo root>
    return pathlib.Path(__file__).resolve().parents[2]


def test_config_registry_matches_schema():
    root = repo_root()
    registry_path = root / "tachyonic" / "consciousness" / "config_registry.json"
    schema_path = root / "tachyonic" / "consciousness" / "schemas" / "config_registry.v1.json"

    assert registry_path.exists(), f"Registry not found: {registry_path}"
    assert schema_path.exists(), f"Schema not found: {schema_path}"

    registry = json5.load(open(registry_path, "r", encoding="utf-8"))
    schema = json.load(open(schema_path, "r", encoding="utf-8"))

    # Will raise jsonschema.exceptions.ValidationError on failure
    jsonschema.validate(instance=registry, schema=schema)
