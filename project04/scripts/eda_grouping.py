#!/usr/bin/env python3
"""EDA: group the todos by user and compare completion rates."""

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


def todos_per_user(df):
    """Series: user_id -> number of todos."""
    return df.groupby("user_id")["id"].count()


def completion_rate_per_user(df):
    """Series: user_id -> fraction of todos completed.

    completed_int is 0/1, so its mean is the completion rate.
    """
    return df.groupby("user_id")["completed_int"].mean()


def user_summary(df):
    """One DataFrame with counts, completed, and rate per user."""
    summary = df.groupby("user_id").agg(
        todos=("id", "count"),
        completed=("completed_int", "sum"),
        rate=("completed_int", "mean"),
    )
    return summary.sort_values("rate", ascending=False)
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    counts = todos_per_user(df)
    rates = completion_rate_per_user(df)

    print("=== todos per user ===")
    print(counts)

    print("\n=== completion rate per user ===")
    print(rates.round(3))

    print("\n=== summary, sorted by completion rate ===")
    print(user_summary(df).round(3))

    # idxmax gives the index label of the largest value, not the value
    top_count = counts.idxmax()
    print(f"\nMost todos: user {top_count} ({counts.max()} todos)")

    # ties matter - there may be more than one user at the top rate
    best_rate = rates.max()
    best_users = rates[rates == best_rate].index.tolist()
    print(f"Highest completion rate: {best_rate:.3f}")
    print(f"Achieved by user(s): {best_users}")


if __name__ == "__main__":
    main()
