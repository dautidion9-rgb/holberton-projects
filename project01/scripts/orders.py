#!/usr/bin/env python3
"""Parsing and statistics for order records.

An "order" here is a plain dict with keys:
    order_id (int), customer (str), product (str),
    quantity (int), price (float)

This is deliberately the same shape a JSON record would have, so the
statistics functions below work unchanged on JSON input later.
"""

import sys

DEFAULT_PATH = "data/sample_orders.txt"

FIELDS = ("order_id", "customer", "product", "quantity", "price")


def parse_order_line(line):
    """Parse one pipe-delimited data row into an order dict.

    Returns None if the line is blank or malformed.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split("|")
    if len(parts) != len(FIELDS):
        return None

    order_id, customer, product, quantity, price = parts

    try:
        return {
            "order_id": int(order_id),
            "customer": customer.strip(),
            "product": product.strip(),
            "quantity": int(quantity),
            "price": float(price),
        }
    except ValueError:
        return None


def load_orders(path, limit=None):
    """Read a pipe-delimited file and return (orders, invalid_count).

    `orders` is a list of dicts - the same structure json.load() would give.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {path}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print(f"Error: file is empty: {path}", file=sys.stderr)
        sys.exit(1)

    orders = []
    invalid = 0

    for line in lines[1:]:          # skip header
        if limit is not None and len(orders) >= limit:
            break
        if not line.strip():
            continue

        order = parse_order_line(line)
        if order is None:
            invalid += 1
        else:
            orders.append(order)

    return orders, invalid


def order_total(order):
    """Revenue contributed by a single order."""
    return order["quantity"] * order["price"]


def summarize(orders):
    """Aggregate a list of order dicts into a stats dict."""
    return {
        "count": len(orders),
        "total_quantity": sum(o["quantity"] for o in orders),
        "total_revenue": sum(order_total(o) for o in orders),
    }


def totals_by(orders, key):
    """Group revenue by any field, e.g. key='customer' or key='product'.

    Returns a dict mapping field value -> revenue, sorted high to low.
    """
    grouped = {}
    for order in orders:
        grouped[order[key]] = grouped.get(order[key], 0.0) + order_total(order)

    return dict(sorted(grouped.items(), key=lambda kv: kv[1], reverse=True))