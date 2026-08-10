#!/usr/bin/env python3
"""Load step: write cleaned records to CSV."""

import csv
import sys

DEFAULT_OUTPUT = "data/todos_clean.csv"

FIELDNAMES = ["id", "user_id", "title", "completed", "completed_int", "title_length"]


def to_csv_row(record):
    """Map an internal record to the CSV schema (camelCase -> snake_case)."""
    return {
        "id": record["id"],
        "user_id": record["userId"],
        "title": record["title"],
        "completed": record["completed"],
        "completed_int": record["completed_int"],
        "title_length": record["title_length"],
    }


def load_to_csv(records, output_path):
    """Write records to CSV with an explicit header. Returns rows written."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow(to_csv_row(record))

    return len(records)


def main():
    sample = [
        {
            "id": 1,
            "userId": 1,
            "title": "Hello World",
            "completed": True,
            "completed_int": 1,
            "title_length": 11,
        }
    ]

    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_out.csv"
    n = load_to_csv(sample, path)
    print(f"Wrote {n} rows to {path}")

    with open(path, encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()