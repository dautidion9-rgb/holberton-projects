#!/usr/bin/env python3
"""EDA step 1: load the cleaned todos CSV and get acquainted with it."""

import sys

import pandas as pd

DEFAULT_PATH = "data/todos_clean.csv"


def load_df(path):
    """Read the cleaned CSV into a DataFrame."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    print("=== head ===")
    print(df.head())

    print("\n=== shape ===")
    print(f"{df.shape[0]} rows, {df.shape[1]} columns")

    print("\n=== dtypes ===")
    print(df.dtypes)

    print("\n=== info ===")
    df.info()

    print("\n=== columns ===")
    print(list(df.columns))


if __name__ == "__main__":
    main()
