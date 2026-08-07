#!/usr/bin/env python3
"""Compute order statistics from a pipe-delimited file, with CLI options."""

import argparse
import sys

DEFAULT_PATH = "data/sample_orders.txt"


def parse_order_line(line):
    """Split one data row into its typed fields.

    Returns a dict, or None if the line is blank or malformed.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split("|")
    if len(parts) != 5:
        return None

    order_id, customer, product, quantity, price = parts

    try:
        return {
            "order_id": int(order_id),
            "customer": customer,
            "product": product,
            "quantity": int(quantity),
            "price": float(price),
        }
    except ValueError:
        return None


def compute_stats(lines, limit=None):
    """Accumulate totals over data rows. Expects `lines` WITHOUT the header.

    Returns a dict of results. Pure logic - no file I/O, no printing.
    """
    stats = {
        "processed": 0,
        "invalid": 0,
        "total_quantity": 0,
        "total_revenue": 0.0,
    }

    for line in lines:
        if limit is not None and stats["processed"] >= limit:
            break

        if not line.strip():
            continue

        order = parse_order_line(line)
        if order is None:
            stats["invalid"] += 1
            continue

        stats["processed"] += 1
        stats["total_quantity"] += order["quantity"]
        stats["total_revenue"] += order["quantity"] * order["price"]

    return stats


def read_data_lines(path):
    """Read the file and return everything after the header row."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error: could not read {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        sys.exit(1)

    return lines[1:]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Compute totals from a pipe-delimited orders file."
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the input file (default: {DEFAULT_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="maximum number of valid data rows to process",
    )
    return parser


def main():
    args = build_parser().parse_args()

    if args.limit is not None and args.limit < 0:
        print("Error: --limit must be zero or positive", file=sys.stderr)
        sys.exit(2)

    data_lines = read_data_lines(args.file)
    stats = compute_stats(data_lines, limit=args.limit)

    print(f"File: {args.file}")
    if args.limit is not None:
        print(f"Row limit: {args.limit}")
    print(f"Rows processed: {stats['processed']}")
    print(f"Rows invalid: {stats['invalid']}")
    print(f"Total quantity: {stats['total_quantity']}")
    print(f"Total revenue: {stats['total_revenue']:.2f}")


if __name__ == "__main__":
    main()