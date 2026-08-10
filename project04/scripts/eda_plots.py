#!/usr/bin/env python3
"""EDA: build and save simple figures."""

import os
import sys

import matplotlib
matplotlib.use("Agg")   # no display needed - write straight to file

import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_PATH = "data/todos_clean.csv"
FIG_DIR = "figures"


def load_df(path):
    """Read the cleaned CSV into a DataFrame."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)


def save(fig, name):
    """Save a figure into FIG_DIR and close it."""
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")
    return path


def plot_title_length_hist(df):
    """Distribution of title lengths."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["title_length"], bins=20, edgecolor="black")
    ax.set_xlabel("Title length (characters)")
    ax.set_ylabel("Number of todos")
    ax.set_title("Distribution of todo title lengths")
    ax.axvline(df["title_length"].mean(), color="red",
               linestyle="--", label=f"mean = {df['title_length'].mean():.1f}")
    ax.legend()
    return save(fig, "title_length_hist.png")
def plot_completion_bar(df):
    """Completed vs pending, overall."""
    counts = df["completed_int"].value_counts().sort_index()
    labels = ["Pending", "Completed"]

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(labels, counts.values, color=["#c44", "#4a4"])
    ax.set_ylabel("Number of todos")
    ax.set_title("Completed vs pending todos")

    for bar, value in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1,
                str(value), ha="center")

    return save(fig, "completion_bar.png")


def plot_completion_by_user(df):
    """Completion rate for each user."""
    rates = df.groupby("user_id")["completed_int"].mean()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(rates.index.astype(str), rates.values, color="#47a")
    ax.axhline(df["completed_int"].mean(), color="red", linestyle="--",
               label=f"overall = {df['completed_int'].mean():.2f}")
    ax.set_xlabel("User ID")
    ax.set_ylabel("Completion rate")
    ax.set_title("Completion rate by user")
    ax.set_ylim(0, 1)
    ax.legend()

    return save(fig, "completion_by_user_bar.png")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    df = load_df(path)

    plot_title_length_hist(df)
    plot_completion_bar(df)
    plot_completion_by_user(df)

    print(f"\n{len(os.listdir(FIG_DIR))} files in {FIG_DIR}/")


if __name__ == "__main__":
    main()
