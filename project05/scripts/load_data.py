#!/usr/bin/env python3
"""Load the four JSONPlaceholder resources into memory.

This module only does I/O. Everything downstream can assume it is
handed plain Python lists of dicts.
"""

import json
import os
import sys

DEFAULT_DIR = "data"

RESOURCES = ("users", "posts", "comments", "todos")


def load_json(path):
    """Read one JSON file and return the parsed object."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def load_users(path):
    """List of user records."""
    return load_json(path)


def load_posts(path):
    """List of post records."""
    return load_json(path)


def load_comments(path):
    """List of comment records."""
    return load_json(path)


def load_todos(path):
    """List of todo records."""
    return load_json(path)


def load_all(data_dir=DEFAULT_DIR):
    """Return {"users": [...], "posts": [...], "comments": [...], "todos": [...]}."""
    return {
        name: load_json(os.path.join(data_dir, f"{name}.json"))
        for name in RESOURCES
    }
def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    print(f"Loaded from {data_dir}/\n")
    for name in RESOURCES:
        records = data[name]
        print(f"{name:9} {len(records):>4} records")
        print(f"          keys: {list(records[0].keys())}")

    print("\nJoin keys:")
    print(f"  posts    -> userId  present: {'userId' in data['posts'][0]}")
    print(f"  todos    -> userId  present: {'userId' in data['todos'][0]}")
    print(f"  comments -> userId  present: {'userId' in data['comments'][0]}")
    print(f"  comments -> postId  present: {'postId' in data['comments'][0]}")

    assert len(data["users"]) == 10
    assert len(data["posts"]) == 100
    assert len(data["comments"]) == 500
    assert len(data["todos"]) == 200
    print("\nRecord counts as expected.")


if __name__ == "__main__":
    main()