#!/usr/bin/env python3
"""Print a summary of a pipe-delimited data file."""

import sys

DEFAULT_PATH = "data/sample_orders.txt"


def read_lines(path):
    """Read a file into a list of lines with trailing newlines stripped.

    Exits with a non-zero code if the file cannot be read or is empty.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {path}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        sys.exit(1)

    return lines


def print_file_info(path, sample_rows=3):
    """Print line count, header, and the first few data rows of a file."""
    lines = read_lines(path)

    print(f"File: {path}")
    print(f"Total lines: {len(lines)}")
    print(f"Header: {lines[0]}")

    print(f"First {sample_rows} data rows:")
    for i, row in enumerate(lines[1:1 + sample_rows], start=1):
        print(f"  {i}. {row}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    print_file_info(path)


if __name__ == "__main__":
    main()