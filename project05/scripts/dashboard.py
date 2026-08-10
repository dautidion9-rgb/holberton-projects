#!/usr/bin/env python3
"""CLI dashboard for exploring user activity metrics."""

import sys

from load_data import load_all
from user_metrics import compute_user_metrics

DEFAULT_DIR = "data"

# metric key -> (label, format spec)
METRICS = {
    "posts": ("num_posts", "Posts", "{}"),
    "comments": ("num_comments_on_posts", "Comments received", "{}"),
    "todos": ("num_todos", "Todos", "{}"),
    "completion": ("completion_rate", "Completion rate", "{:.1%}"),
    "engagement": ("engagement", "Engagement (comments/post)", "{:.2f}"),
}

MENU = """
--- user activity dashboard ---
1  posts per user
2  comments received per user
3  completion rate
4  engagement score
5  full table
6  top 3 for every metric
q  quit
"""

CHOICES = {
    "1": "posts",
    "2": "comments",
    "3": "completion",
    "4": "engagement",
}


def add_engagement(rows):
    """Comments received per post. max(posts, 1) avoids dividing by zero."""
    for r in rows:
        r["engagement"] = r["num_comments_on_posts"] / max(r["num_posts"], 1)
    return rows


def show_metric(rows, metric):
    """Print users ranked by one metric, flagging ties."""
    field, label, fmt = METRICS[metric]
    ordered = sorted(rows, key=lambda r: r[field], reverse=True)

    print(f"\n{label}")
    print("-" * 44)
    for i, r in enumerate(ordered, start=1):
        value = fmt.format(r[field])
        print(f"{i:>3}. {r['user_name'][:26]:<26} {value:>10}")

    values = {r[field] for r in rows}
    if len(values) == 1:
        print(f"\n  note: all users have the same value - ranking is arbitrary")


def show_top3(rows):
    """Top 3 for each metric, with tie warnings."""
    for metric in METRICS:
        field, label, fmt = METRICS[metric]
        ordered = sorted(rows, key=lambda r: r[field], reverse=True)

        print(f"\n{label}")
        values = {r[field] for r in rows}
        if len(values) == 1:
            print(f"  all tied at {fmt.format(ordered[0][field])} - no top 3")
            continue

        for i, r in enumerate(ordered[:3], start=1):
            print(f"  {i}. {r['user_name'][:26]:<26} "
                  f"{fmt.format(r[field]):>10}")


def show_table(rows):
    """The full metrics table."""
    header = (f"{'id':>3} {'name':<24} {'posts':>6} {'comm':>6} "
              f"{'todos':>6} {'rate':>7} {'engage':>7}")
    print("\n" + header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['user_id']:>3} {r['user_name'][:24]:<24} "
              f"{r['num_posts']:>6} {r['num_comments_on_posts']:>6} "
              f"{r['num_todos']:>6} {r['completion_rate']:>6.1%} "
              f"{r['engagement']:>7.2f}")


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    rows = compute_user_metrics(
        data["users"], data["posts"], data["comments"], data["todos"]
    )
    add_engagement(rows)

    print(f"Loaded metrics for {len(rows)} users")

    while True:
        print(MENU)
        try:
            choice = input("choice: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break

        if choice in ("q", "quit", "exit"):
            print("bye")
            break

        if choice in CHOICES:
            show_metric(rows, CHOICES[choice])
        elif choice == "5":
            show_table(rows)
        elif choice == "6":
            show_top3(rows)
        else:
            print(f"  unknown option: {choice!r}")


if __name__ == "__main__":
    main()

# end of file - buffer
# end of file - buffer