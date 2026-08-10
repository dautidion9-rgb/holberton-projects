#!/usr/bin/env python3
"""Generate a user activity report from the JSONPlaceholder datasets."""

import csv
import os
import sys

from load_data import load_all
from user_metrics import compute_user_metrics

DEFAULT_DIR = "data"
CSV_NAME = "user_metrics.csv"

FIELDNAMES = [
    "user_id", "user_name", "username", "num_posts",
    "num_comments_on_posts", "num_todos", "num_completed",
    "completion_rate",
]


def top_by(rows, field):
    """Return (best_value, [rows achieving it]).

    Returns every tied row, not just the first. On this dataset most
    fields are tied across all users, so reporting one winner would
    be misleading.
    """
    best = max(r[field] for r in rows)
    return best, [r for r in rows if r[field] == best]


def describe_top(rows, field, label, fmt="{}"):
    """Print the leader(s) for one field, flagging ties."""
    best, leaders = top_by(rows, field)
    names = ", ".join(r["user_name"] for r in leaders)

    print(f"{label}: {fmt.format(best)}")
    if len(leaders) == 1:
        print(f"  {names}")
    elif len(leaders) == len(rows):
        print(f"  all {len(rows)} users are tied - this ranking is meaningless")
    else:
        print(f"  tied ({len(leaders)}): {names}")


def average_completion_rate(rows):
    """Mean of the per-user rates."""
    return sum(r["completion_rate"] for r in rows) / len(rows)


def overall_completion_rate(rows):
    """Completed todos / all todos - weighted by how many each user has."""
    done = sum(r["num_completed"] for r in rows)
    total = sum(r["num_todos"] for r in rows)
    return done / total if total else 0.0


def write_csv(rows, path):
    """Write the metrics table to CSV."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in FIELDNAMES})
    return len(rows)


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    rows = compute_user_metrics(
        data["users"], data["posts"], data["comments"], data["todos"]
    )

    print("=" * 60)
    print("USER ACTIVITY REPORT")
    print("=" * 60)

    print(f"\nUsers:    {len(rows)}")
    print(f"Posts:    {sum(r['num_posts'] for r in rows)}")
    print(f"Comments: {sum(r['num_comments_on_posts'] for r in rows)}")
    print(f"Todos:    {sum(r['num_todos'] for r in rows)}")

    print(f"\nAverage completion rate: {average_completion_rate(rows):.1%}")
    print(f"Overall completion rate: {overall_completion_rate(rows):.1%}")

    print("\n--- leaders ---")
    describe_top(rows, "num_posts", "Most posts")
    describe_top(rows, "num_comments_on_posts", "Most comments received")
    describe_top(rows, "completion_rate", "Highest completion rate", "{:.1%}")

    print("\n--- ranked by completion rate ---")
    ranked = sorted(rows, key=lambda r: r["completion_rate"], reverse=True)
    for i, r in enumerate(ranked, start=1):
        print(f"{i:>3}. {r['user_name'][:24]:<24} {r['completion_rate']:>6.1%}")

    csv_path = os.path.join(data_dir, CSV_NAME)
    n = write_csv(rows, csv_path)
    print(f"\nWrote {n} rows to {csv_path}")


if __name__ == "__main__":
    main()

# end of file - buffer
# end of file - buffer