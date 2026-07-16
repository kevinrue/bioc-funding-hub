#!/usr/bin/env python3
"""Validate frontmatter of changed funding-hub content files against the JSON Schemas.

Usage: python scripts/validate_frontmatter.py <file> [<file> ...]
"""
import sys
import json
import re
from pathlib import Path
from datetime import date, datetime

import frontmatter
import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {
    "funding-records": json.loads((REPO_ROOT / "schemas/funding-record.schema.json").read_text()),
    "funding-opportunities": json.loads((REPO_ROOT / "schemas/funding-opportunity.schema.json").read_text()),
}
SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def collection_for(path: Path):
    parts = path.parts
    if "funding-records" in parts:
        return "funding-records"
    if "funding-opportunities" in parts:
        return "funding-opportunities"
    return None


def stringify_dates(value):
    """PyYAML auto-parses unquoted YYYY-MM-DD frontmatter values into date/datetime
    objects, but the JSON Schemas declare them as strings (JSON has no date type).
    Normalize recursively before validation."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [stringify_dates(v) for v in value]
    return value


def validate_file(path: Path) -> list:
    errors = []
    post = frontmatter.load(path)
    coll = collection_for(path)
    if coll is None:
        return errors

    meta = stringify_dates(post.metadata)

    schema = SCHEMAS[coll]
    try:
        jsonschema.validate(
            instance=meta,
            schema=schema,
            format_checker=jsonschema.FormatChecker(),
        )
    except jsonschema.ValidationError as e:
        errors.append(f"{path}: schema error: {e.message}")
        return errors
    stem = path.stem

    if meta.get("slug") != stem:
        errors.append(f"{path}: `slug` ({meta.get('slug')!r}) must match filename ({stem!r})")
    if not SLUG_RE.match(stem):
        errors.append(f"{path}: filename must be lowercase alphanumeric+hyphen only")

    if coll == "funding-records":
        try:
            if date.fromisoformat(str(meta["end_date"])) < date.fromisoformat(str(meta["start_date"])):
                errors.append(f"{path}: `end_date` is before `start_date`")
        except (KeyError, ValueError) as e:
            errors.append(f"{path}: invalid date fields: {e}")
        if meta.get("consent_confirmed") is not True:
            errors.append(f"{path}: `consent_confirmed` must be true before merging")

    if coll == "funding-opportunities":
        if meta.get("deadline_type") == "fixed" and not meta.get("deadline"):
            errors.append(f"{path}: `deadline` is required when `deadline_type: fixed`")
        if meta.get("amount_min") is None and meta.get("amount_max") is None:
            errors.append(f"{path}: at least one of `amount_min`/`amount_max` is required")

    if coll == "funding-records":
        related = meta.get("related_opportunity")
        if related and not any((REPO_ROOT / "funding-opportunities").rglob(f"{related}.md")):
            print(f"  [warn] {path}: `related_opportunity: {related}` does not resolve to an existing file")

    return errors


def main(files) -> int:
    all_errors = []
    for f in files:
        p = Path(f)
        if p.suffix == ".md" and collection_for(p) and "_templates" not in p.parts:
            all_errors.extend(validate_file(p))
    if all_errors:
        print("Frontmatter validation failed:\n")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print("All changed content files passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
