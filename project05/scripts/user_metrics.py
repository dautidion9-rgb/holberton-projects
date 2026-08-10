#!/usr/bin/env python3
"""Build user-centric indices by joining posts, comments, and todos."""

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


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    data = load_all(data_dir)

    idx = build_all_indices(data)
    user_posts = idx["user_posts"]
    user_todos = idx["user_todos"]
    user_comments = idx["user_comments"]

    print(f"{'user':>5} {'posts':>6} {'comments':>9} {'todos':>6}")
    for user in data["users"]:
        uid = user["id"]
        print(f"{uid:>5} "
              f"{len(user_posts.get(uid, [])):>6} "
              f"{len(user_comments.get(uid, [])):>9} "
              f"{len(user_todos.get(uid, [])):>6}")

    total_posts = sum(len(v) for v in user_posts.values())
    total_comments = sum(len(v) for v in user_comments.values())
    total_todos = sum(len(v) for v in user_todos.values())

    print(f"\ntotals: {total_posts} posts, {total_comments} comments, "
          f"{total_todos} todos")

    assert total_posts == len(data["posts"])
    assert total_comments == len(data["comments"])
    assert total_todos == len(data["todos"])
    print("Join preserved every record.")


if __name__ == "__main__":
    main()

# end of file - buffer line
# end of file - buffer line