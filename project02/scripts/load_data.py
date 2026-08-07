#!/usr/bin/env python3
"""Load and inspect the todos JSON dataset."""

import json
import sys

DEFAULT_PATH = "data/todos.json"


def load_todos(path):
    """Open a JSON file and return the parsed Python object."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    data = load_todos(path)

    print(f"File: {path}")
    print(f"Top-level type: {type(data).__name__}")
    print(f"Total records: {len(data)}")
    print(f"Keys in first record: {list(data[0].keys())}")


if __name__ == "__main__":
    main()