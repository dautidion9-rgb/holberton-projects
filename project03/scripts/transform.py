#!/usr/bin/env python3
"""Transform step: clean and enrich extracted records.

transform_todos() is pure - data in, data out, no file access.
That is what makes it testable with hand-written input.
"""

import sys


def transform_todo(record):
    """Clean a single record and return a NEW dict.

    Does not modify the input record.
    """
    title = record["title"].strip()
    completed = bool(record["completed"])

    return {
        "id": int(record["id"]),
        "userId": int(record["userId"]),
        "title": title,
        "completed": completed,
        "completed_int": int(completed),
        "title_length": len(title),
    }


def transform_todos(records):
    """Apply transform_todo to every record."""
    return [transform_todo(r) for r in records]


def main():
    # tested with hand-written data, not the file - this function is pure
    sample = [
        {"id": 1, "userId": 1, "title": "  Hello World  ", "completed": True},
        {"id": 2, "userId": 2, "title": "already clean", "completed": False},
    ]

    out = transform_todos(sample)
    for row in out:
        print(row)

    # the input must be unchanged - proves the function is pure
    assert sample[0]["title"] == "  Hello World  "
    assert out[0]["title_length"] == 11
    assert out[0]["completed_int"] == 1
    assert out[1]["completed_int"] == 0
    print("\nTransform checks passed.")


if __name__ == "__main__":
    main()s