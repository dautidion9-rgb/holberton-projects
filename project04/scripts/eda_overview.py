#!/usr/bin/env python3
"""EDA: load the cleaned todos CSV, inspect it, and summarise it."""

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


def overview(df):
    """First look at the data: shape, types, sample rows."""
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


def describe_numeric(df):
    """Summary statistics for the numeric columns."""
    print("=== describe (numeric) ===")
    print(df.describe())

    print("\n=== title_length detail ===")
    lengths = df["title_length"]
    print(f"min:    {lengths.min()}")
    print(f"max:    {lengths.max()}")
    print(f"mean:   {lengths.mean():.1f}")
    print(f"median: {lengths.median()}")
    print(f"std:    {lengths.std():.1f}")
def completion_counts(df):
    """Distribution of the completion flag."""
    print("=== completed: counts ===")
    print(df["completed"].value_counts())

    print("\n=== completed: proportions ===")
    print(df["completed"].value_counts(normalize=True).round(3))

    print(f"\ncompleted_int mean: {df['completed_int'].mean():.3f}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    overview(df)
    print()
    describe_numeric(df)
    print()
    completion_counts(df)


if __name__ == "__main__":
    main()
