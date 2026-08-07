#!/usr/bin/env python3
"""Toolbox entry point: routes subcommands to the utilities in scripts/."""

import argparse
import sys

from scripts.print_file_info import print_file_info
from scripts.order_stats_cli import DEFAULT_PATH, compute_stats, read_data_lines


def cmd_info(args):
    """Handle: toolbox.py info [PATH]"""
    print_file_info(args.path, sample_rows=args.rows)


def cmd_stats(args):
    """Handle: toolbox.py stats [--file PATH] [--limit N]"""
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


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolbox.py",
        description="Utilities for working with pipe-delimited order files.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_info = subparsers.add_parser("info", help="summarize a data file")
    p_info.add_argument(
        "path",
        nargs="?",
        default=DEFAULT_PATH,
        help=f"path to the input file (default: {DEFAULT_PATH})",
    )
    p_info.add_argument(
        "--rows",
        type=int,
        default=3,
        help="how many sample data rows to show (default: 3)",
    )
    p_info.set_defaults(func=cmd_info)

    p_stats = subparsers.add_parser("stats", help="compute order totals")
    p_stats.add_argument(
        "--file",
        default=DEFAULT_PATH,
        help=f"path to the input file (default: {DEFAULT_PATH})",
    )
    p_stats.add_argument(
        "--limit",
        type=int,
        default=None,
        help="maximum number of valid data rows to process",
    )
    p_stats.set_defaults(func=cmd_stats)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # No subcommand given: show help rather than failing silently.
    if args.command is None:
        parser.print_help()
        sys.exit(2)

    args.func(args)


if __name__ == "__main__":
    main()
    