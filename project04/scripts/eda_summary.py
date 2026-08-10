#!/usr/bin/env python3
"""EDA: one consolidated summary of the cleaned todos dataset."""

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


def overall_completion_rate(df):
    """Fraction of todos completed. Mean of a 0/1 column is the rate."""
    return df["completed_int"].mean()


def top_users_by_count(df, n=3):
    """Series of the n users with the most todos."""
    return df.groupby("user_id")["id"].count().sort_values(ascending=False).head(n)


def has_ties_at_cutoff(df, n=3):
    """True if more users share the cutoff count than fit in the top n."""
    counts = df.groupby("user_id")["id"].count().sort_values(ascending=False)
    if len(counts) <= n:
        return False
    return counts.iloc[n - 1] == counts.iloc[n]
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    print("=== shape ===")
    print(f"{df.shape[0]} rows, {df.shape[1]} columns")
    print(f"columns: {list(df.columns)}")

    print("\n=== describe ===")
    print(df.describe().round(2))

    rate = overall_completion_rate(df)
    completed = int(df["completed_int"].sum())
    total = len(df)

    print("\n=== overall completion ===")
    print(f"completed: {completed} / {total}")
    print(f"rate:      {rate:.1%}")

    print("\n=== top 3 users by todo count ===")
    top = top_users_by_count(df, 3)
    for uid, count in top.items():
        print(f"  user {uid:>2}: {count} todos")

    if has_ties_at_cutoff(df, 3):
        print("  (note: counts are tied at the cutoff - this top 3 is arbitrary)")

    print("\n=== top 3 users by completion rate ===")
    rates = df.groupby("user_id")["completed_int"].mean().sort_values(ascending=False)
    for uid, r in rates.head(3).items():
        print(f"  user {uid:>2}: {r:.1%}")

    assert completed + int((df["completed_int"] == 0).sum()) == total
    print("\nCounts reconcile.")


if __name__ == "__main__":
    main()
