#!/usr/bin/env python3
"""EDA: answer questions by filtering rows with boolean indexing."""

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


def long_titles(df, threshold):
    """Rows where title_length is above the threshold."""
    return df[df["title_length"] > threshold]


def completed_vs_pending(df):
    """Return (completed_count, pending_count)."""
    completed = df[df["completed_int"] == 1]
    pending = df[df["completed_int"] == 0]
    return len(completed), len(pending)


def user_breakdown(df, user_id):
    """Completed and pending counts for one user."""
    user_rows = df[df["user_id"] == user_id]

    done = df[(df["user_id"] == user_id) & (df["completed_int"] == 1)]
    todo = df[(df["user_id"] == user_id) & (df["completed_int"] == 0)]

    return {
        "total": len(user_rows),
        "completed": len(done),
        "pending": len(todo),
    }


def long_and_pending(df, threshold):
    """Long titles that are still unfinished - two conditions with &."""
    return df[(df["title_length"] > threshold) & (df["completed_int"] == 0)]
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    threshold = 40

    print(f"=== titles longer than {threshold} chars ===")
    long_rows = long_titles(df, threshold)
    print(f"{len(long_rows)} of {len(df)} todos")
    print(long_rows[["id", "user_id", "title_length", "completed"]].head())

    done, pending = completed_vs_pending(df)
    print(f"\n=== completion ===")
    print(f"completed: {done}")
    print(f"pending:   {pending}")
    print(f"total:     {done + pending}")

    print("\n=== per user breakdown ===")
    for uid in sorted(df["user_id"].unique()):
        b = user_breakdown(df, uid)
        print(f"  user {uid:>2}: {b['completed']:>2} done, "
              f"{b['pending']:>2} pending, {b['total']:>2} total")

    combo = long_and_pending(df, threshold)
    print(f"\n=== long AND pending ===")
    print(f"{len(combo)} todos are both over {threshold} chars and unfinished")
    if not combo.empty:
        print(combo[["id", "user_id", "title_length"]].head())

    # the counts must add up - cheap integrity check
    assert done + pending == len(df)
    print("\nCounts reconcile.")


if __name__ == "__main__":
    main()
