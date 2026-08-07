#!/usr/bin/env python3
"""Queries over the todos dataset: filtering and aggregating by user.

Contains two implementations of the same queries: one that scans the
list each time, and one that uses the indices from indexing.py. The
asserts at the bottom of main() check that both agree.
"""

import sys

from load_data import load_todos
from indexing import (
    build_user_index,
    build_completion_index,
    count_completed_by_user_indexed,
    get_todos_by_user_indexed,
    get_users_with_all_completed_indexed,
)

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
    """Return {userId: number of completed todos}."""
    counts = {todo["userId"]: 0 for todo in todos}
    for todo in todos:
        if todo["completed"]:
            counts[todo["userId"]] += 1
    return counts


def get_users_with_all_completed(todos):
    """Return the set of userIds whose todos are ALL completed."""
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

    user_index = build_user_index(todos)
    completion_index = build_completion_index(todos)

    user_1 = get_todos_by_user_indexed(user_index, 1)
    print(f"User 1 has {len(user_1)} todos")
    print(f"First title: {user_1[0]['title']}")

    print(f"\nCompleted: {len(completion_index['completed'])}")
    print(f"Pending:   {len(completion_index['pending'])}")

    completed = count_completed_by_user_indexed(user_index)

    print("\nCompleted per user:")
    for uid in sorted(user_index):
        print(f"  user {uid:>2}: {completed[uid]:>2} / {len(user_index[uid]):>2}")

    done = get_users_with_all_completed_indexed(user_index)
    print(f"\nAll completed: {sorted(done) if done else 'none'}")

    assert get_todos_by_user(todos, 1) == user_1
    assert count_completed_by_user(todos) == completed
    assert get_users_with_all_completed(todos) == done
    print("\nIndexed and scanning results match.")


if __name__ == "__main__":
    main()