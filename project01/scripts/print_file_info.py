#!/usr/bin/env python3
"""Print a summary of a pipe-delimited data file."""

import sys

DEFAULT_PATH = "data/sample_orders.txt"


def main():
    # sys.argv[0] is the script name; anything after is a user argument
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: cannot read file: {path}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"File: {path}")
    print(f"Total lines: {len(lines)}")
    print(f"Header: {lines[0]}")

    print("First 3 data rows:")
    for i, row in enumerate(lines[1:4], start=1):
        print(f"  {i}. {row}")


if __name__ == "__main__":
    main()