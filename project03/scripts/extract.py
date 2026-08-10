#!/usr/bin/env python3
"""Extract step: read raw JSON and keep only the fields we need."""

import json
import sys

DEFAULT_INPUT = "data/raw_todos.json"
FIELDS = ("id", "userId", "title", "completed")


def extract_todos(input_path):
    """Read raw JSON and return a list of dicts with only FIELDS."""
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {input_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    return [{k: record[k] for k in FIELDS} for record in data]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    records = extract_todos(path)

    print(f"Extracted {len(records)} records from {path}")
    print(f"Fields kept: {list(records[0].keys())}")
    print(f"First record: {records[0]}")


if __name__ == "__main__":
    main()
    