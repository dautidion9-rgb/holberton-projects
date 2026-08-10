#!/usr/bin/env python3
"""Plot user activity metrics and save the figures."""

import os
import sys

import matplotlib
matplotlib.use("Agg")   # no display in WSL - write straight to file

import matplotlib.pyplot as plt

from load_data import load_all
from user_metrics import compute_user_metrics

DEFAULT_DIR = "data"
FIG_DIR = "figures"


def save(fig, name):
    """Save a figure into FIG_DIR and close it."""
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")
    return path


def plot_user_activity(rows):
    """Posts and comments received, side by side per user."""
    ids = [str(r["user_id"]) for r in rows]
    posts = [r["num_posts"] for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(ids, posts, color="#47a")
    ax.set_xlabel("User ID")
    ax.set_ylabel("Number of posts")
    ax.set_title("Posts per user")
    ax.set_ylim(0, max(posts) * 1.3)

    for i, v in enumerate(posts):
        ax.text(i, v + 0.3, str(v), ha="center")

    # every user has the same count - say so on the figure
    if len(set(posts)) == 1:
        ax.text(0.5, 0.92,
                f"every user has exactly {posts[0]} posts - no variation",
                transform=ax.transAxes, ha="center", fontsize=9,
                style="italic", color="#666")

    return save(fig, "user_activity_bar.png")


def plot_completion_rate(rows):
    """Completion rate per user, sorted, with the overall mean marked."""
    ordered = sorted(rows, key=lambda r: r["completion_rate"], reverse=True)
    ids = [str(r["user_id"]) for r in ordered]
    rates = [r["completion_rate"] for r in ordered]

    done = sum(r["num_completed"] for r in rows)
    total = sum(r["num_todos"] for r in rows)
    overall = done / total if total else 0.0

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(ids, rates, color="#4a4")
    ax.axhline(overall, color="red", linestyle="--",
               label=f"overall = {overall:.1%}")
    ax.set_xlabel("User ID (sorted by rate)")
    ax.set_ylabel("Completion rate")
    ax.set_title("Todo completion rate by user")
    ax.set_ylim(0, 1)
    ax.legend()

    for i, v in enumerate(rates):
        ax.text(i, v + 0.02, f"{v:.0%}", ha="center", fontsize=9)

    return save(fig, "completion_rate_bar.png")


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    rows = compute_user_metrics(
        data["users"], data["posts"], data["comments"], data["todos"]
    )

    plot_user_activity(rows)
    plot_completion_rate(rows)

    print(f"\n{len(os.listdir(FIG_DIR))} files in {FIG_DIR}/")


if __name__ == "__main__":
    main()

# end of file - buffer
# end of file - buffer