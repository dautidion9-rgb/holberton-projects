#!/usr/bin/env python3
"""Pipeline: extract -> transform -> load.

Holds no logic of its own. Imports the three steps and runs them in order.
"""

import argparse
import sys

from extract import extract_todos
from transform import transform_todos
from load import load_to_csv

DEFAULT_INPUT = "data/raw_todos.json"
DEFAULT_OUTPUT = "data/todos_clean.csv"


def run_pipeline(input_path, output_path):
    """Run all three steps. Returns (extracted, written)."""
    records = extract_todos(input_path)
    clean_records = transform_todos(records)
    written = load_to_csv(clean_records, output_path)
    return len(records), written


def build_parser():
    parser = argparse.ArgumentParser(
        description="Turn raw todos JSON into a clean CSV."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT,
                        help=f"raw JSON input (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help=f"CSV output (default: {DEFAULT_OUTPUT})")
    return parser


def main():
    args = build_parser().parse_args()

    extracted, written = run_pipeline(args.input, args.output)

    print(f"Input:     {args.input}")
    print(f"Extracted: {extracted} records")
    print(f"Written:   {written} rows")
    print(f"Output:    {args.output}")

    if extracted != written:
        print("Warning: record count changed during the pipeline",
              file=sys.stderr)


if __name__ == "__main__":
    main()