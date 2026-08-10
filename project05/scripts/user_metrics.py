#!/usr/bin/env python3
"""Build user indices and compute per-user activity metrics."""

import sys

from load_data import load_all

DEFAULT_DIR = "data"


def build_post_owner(posts):
    """Return {postId: userId} - the bridge comments need."""
    return {post["id"]: post["userId"] for post in posts}


def group_by(records, key):
    """Generic grouping: {value of key: [records with that value]}."""
    index = {}
    for record in records:
        index.setdefault(record[key], []).append(record)
    return index


def build_user_posts(posts):
    """{userId: [post, ...]}"""
    return group_by(posts, "userId")


def build_user_todos(todos):
    """{userId: [todo, ...]}"""
    return group_by(todos, "userId")


def build_user_comments(comments, posts):
    """{userId: [comment, ...]} - comments received on that user's posts."""
    post_owner = build_post_owner(posts)
    index = {}
    orphans = 0
    for comment in comments:
        owner = post_owner.get(comment["postId"])
        if owner is None:
            orphans += 1
            continue
        index.setdefault(owner, []).append(comment)
    if orphans:
        print(f"warning: {orphans} orphan comments", file=sys.stderr)
    return index


def build_all_indices(data):
    """Return every user-keyed index in one dict."""
    return {
        "user_posts": build_user_posts(data["posts"]),
        "user_todos": build_user_todos(data["todos"]),
        "user_comments": build_user_comments(data["comments"], data["posts"]),
    }


def compute_user_metrics(users, posts, comments, todos):
    """Return a list of per-user metric dicts - one row per user."""
    user_posts = build_user_posts(posts)
    user_todos = build_user_todos(todos)
    user_comments = build_user_comments(comments, posts)

    rows = []

    for user in users:
        uid = user["id"]
        u_posts = user_posts.get(uid, [])
        u_comments = user_comments.get(uid, [])
        u_todos = user_todos.get(uid, [])

        completed = sum(1 for t in u_todos if t["completed"])
        rate = completed / len(u_todos) if u_todos else 0.0

        rows.append({
            "user_id": uid,
            "user_name": user["name"],
            "username": user["username"],
            "num_posts": len(u_posts),
            "num_comments_on_posts": len(u_comments),
            "num_todos": len(u_todos),
            "num_completed": completed,
            "completion_rate": rate,
        })

    return rows


def print_metrics_table(rows):
    """Print the metrics as an aligned text table."""
    header = (f"{'id':>3} {'name':<24} {'posts':>6} {'comments':>9} "
              f"{'todos':>6} {'done':>5} {'rate':>7}")
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['user_id']:>3} {r['user_name'][:24]:<24} "
              f"{r['num_posts']:>6} {r['num_comments_on_posts']:>9} "
              f"{r['num_todos']:>6} {r['num_completed']:>5} "
              f"{r['completion_rate']:>6.1%}")


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    rows = compute_user_metrics(
        data["users"], data["posts"], data["comments"], data["todos"]
    )

    print_metrics_table(rows)

    assert len(rows) == len(data["users"])
    assert sum(r["num_posts"] for r in rows) == len(data["posts"])
    assert sum(r["num_comments_on_posts"] for r in rows) == len(data["comments"])
    assert sum(r["num_todos"] for r in rows) == len(data["todos"])
    print("\nMetrics reconcile with source counts.")


if __name__ == "__main__":
    main()

# end of file - buffer
# end of file - buffer