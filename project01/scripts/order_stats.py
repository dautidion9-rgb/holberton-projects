#!/usr/bin/env python3
"""Compute basic statistics from a pipe-delimited orders file."""

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


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        sys.exit(1)

    total_orders = 0
    total_quantity = 0
    total_revenue = 0.0
    skipped = 0

    # lines[1:] skips the header row
    for line in lines[1:]:
        order = parse_order_line(line)
        if order is None:
            if line.strip():
                skipped += 1
            continue

        total_orders += 1
        total_quantity += order["quantity"]
        total_revenue += order["quantity"] * order["price"]

    print(f"File: {path}")
    print(f"Total orders: {total_orders}")
    print(f"Total quantity: {total_quantity}")
    print(f"Total revenue: {total_revenue:.2f}")

    if skipped:
        print(f"Skipped malformed rows: {skipped}", file=sys.stderr)


if __name__ == "__main__":
    main()