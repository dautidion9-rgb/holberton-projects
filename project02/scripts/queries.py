#!/usr/bin/env python3
"""Queries over the todos dataset: filtering and aggregating by user."""

import sys

from load_data import load_todos

DEFAULT_PATH = "data/todos.json"


def get_todos_by_user(todos, user_id):
    """Return all todo records belonging to one user."""
    return [t for t in todos if t["userId"] == user_id]


def count_todos_by_user(todos):
    """Return {userId: total number of todos}."""
    counts = {}
    for todo in todos:
        uid = todo["userId"]
        counts[uid] = counts.get(uid, 0) + 1
    return counts


def count_completed_by_user(todos):
    """Return {userId: number of completed todos}.

    Every user in the data appears, even if they completed nothing.
    """
    counts = {todo["userId"]: 0 for todo in todos}

    for todo in todos:
        if todo["completed"]:
            counts[todo["userId"]] += 1

    return counts


def get_users_with_all_completed(todos):
    """Return the set of userIds whose todos are ALL completed.

    A user with no todos at all is excluded - `all()` on an empty
    sequence is True, which would otherwise report them as finished.
    """
    totals = count_todos_by_user(todos)
    completed = count_completed_by_user(todos)

    return {
        uid
        for uid in totals
        if totals[uid] > 0 and completed[uid] == totals[uid]
    }


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    todos = load_todos(path)

    user_1 = get_todos_by_user(todos, 1)
    print(f"User 1 has {len(user_1)} todos")
    print(f"First title: {user_1[0]['title']}")

    totals = count_todos_by_user(todos)
    completed = count_completed_by_user(todos)

    print("\nPer user (completed / total):")
    for uid in sorted(totals):
        print(f"  user {uid:>2}: {completed[uid]:>2} / {totals[uid]:>2}")

    done = get_users_with_all_completed(todos)
    print(f"\nUsers with everything completed: {sorted(done) if done else 'none'}")


if __name__ == "__main__":
    main()